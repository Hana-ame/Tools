package mymux

import (
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"sync"

	"github.com/gorilla/websocket"
)

const (
	ERR_BUS_CLOSED = "my bus already closed" // 总线关闭错误信息
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
type MyWsBus struct {
	*websocket.Conn

	sync.Mutex // 仅允许一个读取守护进程读取。
}

// RecvFrame 从 WebSocket 连接接收一帧数据。
func (b *MyWsBus) RecvFrame() (MyFrame, error) {
	_, f, err := b.ReadMessage()
	return MyFrame(f), err
}

// SendFrame 通过 WebSocket 发送一帧数据。
func (b *MyWsBus) SendFrame(f MyFrame) error {
	err := b.WriteMessage(websocket.BinaryMessage, f)
	return err
}

// MyPipeBus 本地管道总线结构。
type MyPipeBus struct {
	MyBusReader
	MyBusWriter

	closed bool // 标记总线是否已关闭
}

// Close 关闭总线，释放相关资源。
func (b *MyPipeBus) Close() error {
	if b.closed {
		return fmt.Errorf(ERR_BUS_CLOSED) // 如果总线已关闭，返回错误
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
