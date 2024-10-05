package mymux

import (
	"encoding/binary"
	"io"
	"net"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

const (
	ERR_BUS_CLOSED Error = "my bus already closed" // 总线关闭错误信息
)

// MyBus 接口定义了读取和写入总线的功能，并包含关闭功能。
type MyBus interface {
	MyBusReader
	MyBusWriter

	io.Closer
}

// MyBusWriter 接口定义了发送帧的功能，并包含关闭功能。
type MyBusWriter interface {
	SendFrame(MyFrame) error

	io.Closer
}

// MyBusReader 接口定义了接收帧的功能，提供锁功能以确保线程安全，并包含关闭功能。
type MyBusReader interface {
	RecvFrame() (MyFrame, error)

	sync.Locker // 仅允许一个读取守护进程读取。

	io.Closer
}

// MyConnBus 用于 TCP 连接的总线结构。
type MyConnBus struct {
	net.Conn

	sync.Mutex // 仅允许一个读取守护进程读取。
}

// RecvFrame 从连接中接收一帧数据。
func (b *MyConnBus) RecvFrame() (MyFrame, error) {
	// 获取帧长度
	l := make([]byte, 2)
	_, err := b.Read(l)
	if err != nil {
		return nil, err
	}
	pl := binary.BigEndian.Uint16(l)
	// 获取帧内容
	f := make([]byte, pl)
	_, err = b.Read(f)
	return MyFrame(f), err
}

// SendFrame 发送一帧数据到连接。
func (b *MyConnBus) SendFrame(f MyFrame) error {
	l := make([]byte, 2)
	binary.BigEndian.PutUint16(l, uint16(len(f)))
	if _, err := b.Write(l); err != nil {
		return err
	}
	if _, err := b.Write(f); err != nil {
		return err
	}
	return nil
}

// MyWsBus 用于 WebSocket 连接的总线结构。
type MyWsBusReader struct {
	*websocket.Conn

	sync.Mutex
}

// MyWsBus 用于 WebSocket 连接的总线结构。
type MyWsBusWriter struct {
	*websocket.Conn

	sync.Mutex
}

type MyWsBus struct {
	*websocket.Conn

	*MyWsBusReader
	*MyWsBusWriter

	sync.Mutex // 仅允许一个读取守护进程读取。
}

func NewWsBus(c *websocket.Conn) MyBus {
	// func NewWsBus(c *websocket.Conn) *MyWsBus {
	return &MyWsBus{
		Conn:          c,
		MyWsBusReader: &MyWsBusReader{Conn: c},
		MyWsBusWriter: &MyWsBusWriter{Conn: c},
	}
}

// RecvFrame 从 WebSocket 连接接收一帧数据。
func (b *MyWsBusReader) RecvFrame() (MyFrame, error) {
	b.Lock()
	defer b.Unlock()
	_, f, err := b.ReadMessage()
	return MyFrame(f), err
}

// SendFrame 通过 WebSocket 发送一帧数据。
func (b *MyWsBusWriter) SendFrame(f MyFrame) error {
	b.Lock()
	defer b.Unlock()
	err := b.WriteMessage(websocket.BinaryMessage, f)
	return err
}

func (b *MyWsBus) Close() error {
	return b.Conn.Close()
}

// MyPipeBus 本地管道总线结构。
type MyPipeBus struct {
	MyBusReader
	MyBusWriter

	closed bool // 标记总线是否已关闭
}

// Close 关闭总线，释放相关资源。
func (b *MyPipeBus) Close() error {
	// const Tag = "MyPipeBus.Close"
	if b.closed {
		// 		debug.E(Tag, "already closed")
		return ERR_BUS_CLOSED
	}
	b.closed = true
	b.MyBusReader.Close() // 关闭读取器
	b.MyBusWriter.Close() // 关闭写入器
	return nil
}

// NewBusFromPipe 创建一个新的管道总线实例。
func NewBusFromPipe(reader MyBusReader, writer MyBusWriter) *MyPipeBus {
	return &MyPipeBus{
		MyBusReader: reader,
		MyBusWriter: writer,
	}
}

// NewPipeBusPair 创建一对本地管道总线。
func NewPipeBusPair() (*MyPipeBus, *MyPipeBus) {
	a2bReader, b2aWriter := NewPipe()              // 创建 a 到 b 的读写管道
	b2aReader, a2bWriter := NewPipe()              // 创建 b 到 a 的读写管道
	a2bBus := NewBusFromPipe(a2bReader, a2bWriter) // 创建 a 到 b 的总线
	b2aBus := NewBusFromPipe(b2aReader, b2aWriter) // 创建 b 到 a 的总线
	return a2bBus, b2aBus
}

// NewDebugPipeBusPair 创建一对带调试信息的本地管道总线。
func NewDebugPipeBusPair(tag string) (*MyPipeBus, *MyPipeBus) {
	a2bReader, b2aWriter := NewDebugPipe(tag)      // 创建带调试信息的管道
	b2aReader, a2bWriter := NewDebugPipe(tag)      // 创建带调试信息的管道
	a2bBus := NewBusFromPipe(a2bReader, a2bWriter) // 创建 a 到 b 的总线
	b2aBus := NewBusFromPipe(b2aReader, b2aWriter) // 创建 b 到 a 的总线
	return a2bBus, b2aBus
}

// 在正常情况下能够传输 见test
// 如果有什么问题遇到的时候再来debug
type ReliableBus struct {
	MyBus

	f      MyFrame
	e      error
	nextId uint8

	*Buffer
	request uint8

	*sync.Cond
}

func NewReliableBus(b MyBus, size uint8) *ReliableBus {
	rb := &ReliableBus{
		MyBus: b,

		Buffer: NewGBNBuffer(size),

		Cond: sync.NewCond(&sync.Mutex{}),
	}

	go rb.ReadDaemon()
	go rb.WriteDeamon()
	go rb.AcknowledgeDeamon()
	return rb
}

func (b *ReliableBus) SendFrame(f MyFrame) error {
	if f.Command() == Disorder || f.Command() == DisorderAcknowledge {
		b.Offer(f)
		return nil
	}
	return b.MyBus.SendFrame(f)
}
func (b *ReliableBus) RecvFrame() (MyFrame, error) {
	b.L.Lock()
	for !(b.f != nil || b.closed) {
		b.Wait()
	}
	if b.closed {
		b.L.Unlock()
		return b.f, ERR_BUS_CLOSED
	}
	f, e := b.f, b.e
	b.f, b.e = nil, nil

	b.L.Unlock()
	b.Broadcast()
	return f, e
}

func (b *ReliableBus) ReadDaemon() {
	// const Tag = "ReliableBus.ReadDaemon"
	for {
		f, e := b.MyBus.RecvFrame()
		// 		debug.T(Tag, "recv Frame", SprintFrame(f))
		b.L.Lock()
		for !(b.f == nil || b.closed) {
			b.Wait()
		}
		if b.closed {
			b.L.Unlock()
			return
		}
		if f.Command() == Disorder {
			// 如果是disorder，那么在bus处处理。
			if f.SequenceNumber() == b.nextId {
				b.f, b.e = f, e
				b.nextId++
				// 				debug.T(Tag, "b.nextid = ", b.nextId)
			}
		}
		if f.Command() == DisorderAcknowledge || f.Command() == Disorder {
			// 			debug.T(Tag, b.request, " should set to ", f.AcknowledgeNumber())
			if b.request-f.AcknowledgeNumber() > b.size {
				// 				debug.T(Tag, b.request, " set to ", f.AcknowledgeNumber())
				b.request = f.AcknowledgeNumber()
				b.Buffer.SetTail(b.request)
			}
		} else {
			b.f, b.e = f, e
		}

		b.L.Unlock()
		b.Broadcast()
	}
}
func (b *ReliableBus) WriteDeamon() {
	// const Tag = "ReliableBus.WriteDeamon"

	for {
		id, data, ok := b.Buffer.Read() // 在buffer里的一定是disorder
		if !ok {
			if b.closed {
				return
			}
			// 			debug.E(Tag, id, data, ok)
			continue
		}
		f := MyFrame(data)
		f.SetSequenceNumber(id)
		f.SetAcknowledgeNumber(b.nextId)

		e := b.MyBus.SendFrame(f)
		if e != nil {
			if b.closed {
				return
			}
			// 			debug.E(Tag, e.Error())
			continue
		}
	}
}

func (b *ReliableBus) AcknowledgeDeamon() {
	for {
		time.Sleep(time.Second)
		f := NewFrame(0, 0, 0, DisorderAcknowledge, 0, b.nextId, nil)
		e := b.MyBus.SendFrame(f)
		if e != nil {
			if b.closed {
				return
			}
			// 				debug.E(Tag, "send frame error", e.Error())
			continue
		}
		// 			debug.T(Tag, "requesting", b.request)
		b.Buffer.SetTail(b.request) // 顺手在这里设置了
	}
}

func (b *ReliableBus) Close() error {
	e := b.MyBus.Close()
	b.Buffer.Close()
	b.closed = true
	b.Broadcast()
	return e
}
