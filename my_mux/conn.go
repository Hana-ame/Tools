package mymux

import (
	"encoding/binary"
	"fmt"
	"io"
	"time"

	"github.com/Hana-ame/udptun/Tools/debug"
)

const (
	ERR_CONN_CLOSED Error = "my frame conn closed"
)

func ErrorIsClosed(e error) bool {
	err := Error(e.Error())
	return err == ERR_BUS_CLOSED || err == ERR_PIPE_CLOSED || err == ERR_CONN_CLOSED
}

type MyFrameConn struct {
	MyBus

	localAddr  Addr
	remoteAddr Addr
	port       uint8

	closed bool

	MTU int // for body
}

func NewFrameConn(bus MyBus, localAddr, remoteAddr Addr, port uint8) *MyFrameConn {
	c := &MyFrameConn{
		MyBus: bus,

		localAddr:  localAddr,
		remoteAddr: remoteAddr,
		port:       port,

		MTU: 1024,
	}
	return c
}

func (c *MyFrameConn) WriteFrame(p []byte) (n int, err error) {
	const Tag = "MyFrameConn.WriteFrame"
	debug.T(Tag, c.localAddr, "->", c.remoteAddr, ":", c.port, string(p))
	if c.closed {
		debug.D(Tag, c.localAddr, "->", c.remoteAddr, ":", c.port, "conn closed")
		err = fmt.Errorf("closed")
		return
	}
	if len(p) > c.MTU {
		p = p[:c.MTU]
	}
	f := NewFrame(c.localAddr, c.remoteAddr, c.port, Disorder, 0, 0, p)

	n = len(p)
	err = c.MyBus.SendFrame(f)
	return
}

// 需要大于MTU
// 从ReadBuf里面取到纯净的Data
func (c *MyFrameConn) ReadFrame() ([]byte, error) {
	const Tag = "MyFrameConn.ReadFrame"
	if c.closed {
		return nil, (ERR_CONN_CLOSED)
	}

	f, err := c.MyBus.RecvFrame()
	if err != nil {
		return nil, err
	}
	debug.T(Tag, c.localAddr, "<-", c.remoteAddr, ":", c.port, f.Command().String())
	if f.Command() == Close {
		defer c.Close()
		return nil, (ERR_CONN_CLOSED)
	}
	debug.T(Tag, c.localAddr, "<-", c.remoteAddr, ":", c.port, string(f.Data()))
	return f.Data(), nil
}

// close
func (c *MyFrameConn) Close() error {
	const Tag = "MyFrameConn.Close"
	debug.D(Tag, c.localAddr, "<-", c.remoteAddr, ":", c.port, "closing")
	defer debug.D(Tag, c.localAddr, "<-", c.remoteAddr, ":", c.port, "closed")

	if c.closed {
		return (ERR_CONN_CLOSED)
	}
	c.SendFrame(NewCtrlFrame(c.localAddr, c.remoteAddr, c.port, Close, 0, 0))
	// time.Sleep(time.Second) // it seems that close cannot send, so sleep and
	c.MyBus.Close()
	// c.MyMux.PrintMap() // debug 加了这句client Close不能
	c.closed = true
	return nil
}

// for net.Conn interface
func (c *MyFrameConn) LocalAddr() Addr {
	return c.localAddr
}
func (c *MyFrameConn) RemoteAddr() Addr {
	return c.remoteAddr
}

func (c *MyFrameConn) SetDeadline(t time.Time) error {
	return fmt.Errorf("todo")
}
func (c *MyFrameConn) SetReadDeadline(t time.Time) error {
	return fmt.Errorf("todo")
}
func (c *MyFrameConn) SetWriteDeadline(t time.Time) error {
	return fmt.Errorf("todo")
}

// 插口，专门把FreamConn转换为io.Streamer
type MyFrameConnStreamer struct {
	*MyFrameConn

	rb []byte
}

func (c *MyFrameConnStreamer) Write(p []byte) (n int, err error) {
	return c.WriteFrame(p)
}

func (c *MyFrameConnStreamer) Read(p []byte) (n int, err error) {
	if len(c.rb) == 0 {
		c.rb, err = c.ReadFrame()
		if err != nil {
			return
		}
	}
	n = copy(p, c.rb)
	c.rb = c.rb[n:]
	return
}

// 这里开始没什么关系，可能用到TCP的东西再说。
type MyConn struct {
	MyBus

	// MyTag

	localAddr  Addr
	remoteAddr Addr
	Port       uint8

	sequenceNumber uint8 // 即将发送的frame的Seq number
	requestingSeq  uint8 // 对方要求的最近的Seq num

	ReadBuf     chan MyFrame // 先做简单的
	nextReadSeq uint8        // 己方维护的自卷积要求的最近的Seq num

	MTU        int
	WindowSize int // 用于更新acknowledgeNumber

	closed bool
}

func NewConn(mux MyBus, frameTag MyTag, localAddr, remoteAddr Addr, port uint8) *MyConn {
	conn := &MyConn{
		MyBus: mux,
		// MyTag:          frameTag,
		localAddr:      localAddr,
		remoteAddr:     remoteAddr,
		Port:           port,
		sequenceNumber: 0,
		requestingSeq:  0,
		ReadBuf:        make(chan MyFrame),
		nextReadSeq:    0,
		MTU:            1024,
		WindowSize:     32,
		closed:         false,
	}
	return conn
}

// c.localAddr, c.remoteAdr, c.port
func (c *MyConn) Tag() MyTag {
	var tag MyTag
	binary.BigEndian.PutUint16(tag[0:2], uint16(c.remoteAddr))
	binary.BigEndian.PutUint16(tag[2:4], uint16(c.localAddr))
	tag[4] = c.Port
	return tag
}

// 会限制不能大于MTU
// 封装成DataFrame从Mux发送
func (c *MyConn) Write(p []byte) (n int, err error) {
	if c.closed {
		err = fmt.Errorf("closed")
		return
	}
	if len(p) > c.MTU {
		p = p[:c.MTU]
	}
	f := NewDataFrame(c.localAddr, c.remoteAddr, c.Port, c.sequenceNumber, c.nextReadSeq, p)

	n = len(p)
	err = c.MyBus.SendFrame(f)
	return
}

// 需要大于MTU
// 从ReadBuf里面取到纯净的Data
func (c *MyConn) Read(p []byte) (n int, err error) {
	if c.closed {
		err = fmt.Errorf("closed")
		return
	}
	f := <-c.ReadBuf

	if f.Command() == Close {
		return 0, io.EOF
	}

	// 不是Close也不是其他frame，DataFrame根据状态来的
	// 更新最后收到的帧
	if f.AcknowledgeNumber()-c.requestingSeq < uint8(c.WindowSize) {
		c.requestingSeq = f.AcknowledgeNumber()
	}
	c.nextReadSeq = f.SequenceNumber() // 这个需要稍后改一下。

	n = copy(p, f.Data())
	return
}

func (c *MyConn) Close() error {
	// debug
	const Tag = "MyConn.Close"
	debug.T(Tag, "closing")
	defer debug.T(Tag, "closed")

	if c.closed {
		return fmt.Errorf("closed")
	}
	// 给ReadBuf发送一个Close的CtrlFrame，读到就直接EOF
	c.ReadBuf <- MyFrame(NewCtrlFrame(0, 0, 0, Close, 0, 0))
	c.SendFrame(NewCtrlFrame(c.localAddr, c.remoteAddr, c.Port, Close, c.sequenceNumber, c.nextReadSeq))
	// c.MyBus.RemoveConn(c)
	c.MyBus.Close()
	// c.MyMux.PrintMap() // debug 加了这句client Close不能
	return nil
}

// for mux
// 从这里接受Frame到缓冲区
func (c *MyConn) PutFrame(f MyFrame) {
	// 及时Close
	if f.Command() == Close {
		c.Close()
		return
	}

	c.ReadBuf <- f
}

// for net.Conn interface
func (c *MyConn) LocalAddr() Addr {
	return c.localAddr
}
func (c *MyConn) RemoteAddr() Addr {
	return c.remoteAddr
}

func (c *MyConn) SetDeadline(t time.Time) error {
	return fmt.Errorf("todo")
}
func (c *MyConn) SetReadDeadline(t time.Time) error {
	return fmt.Errorf("todo")
}
func (c *MyConn) SetWriteDeadline(t time.Time) error {
	return fmt.Errorf("todo")
}
