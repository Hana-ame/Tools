package mymux

import (
	"fmt"
	"io"
	"time"
)

type MyConn struct {
	MyMux

	FrameTag

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

func NewConn(mux MyMux, frameTag FrameTag, localAddr, remoteAddr Addr, port uint8) *MyConn {
	conn := &MyConn{
		MyMux:          mux,
		FrameTag:       frameTag,
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
	err = c.MyMux.SendFrame(f)
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

	copy(p, f.Data())
	return
}

func (c *MyConn) Close() error {
	if c.closed {
		return fmt.Errorf("closed")
	}
	// 给ReadBuf发送一个Close的CtrlFrame，读到就直接EOF
	c.ReadBuf <- DataFrame(NewCtrlFrame(0, 0, 0, Close, 0, 0))
	c.SendFrame(NewCtrlFrame(c.localAddr, c.remoteAddr, c.Port, Close, c.sequenceNumber, c.nextReadSeq))
	c.MyMux.RemoveConn(c)
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

// for net.Conn
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