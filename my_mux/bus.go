package mymux

import (
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"sync"
)

type MyBus interface {
	MyBusReader
	MyBusWriter

	io.Closer
}

type MyBusWriter interface {
	SendFrame(MyFrame) error

	io.Closer
}

type MyBusReader interface {
	RecvFrame() (MyFrame, error)

	sync.Locker // only one read deamon can read.

	io.Closer
}

// 用于TCPConn的bus
type MyConnBus struct {
	net.Conn

	sync.Mutex // only one read deamon can read.
}

// before recv loop, use Lock
func (b *MyConnBus) RecvFrame() (MyFrame, error) {
	// get length
	l := make([]byte, 2)
	_, err := b.Read(l)
	if err != nil {
		return nil, err
	}
	pl := binary.BigEndian.Uint16(l)
	// get frame
	f := make([]byte, pl)
	_, err = b.Read(f)
	return MyFrame(f), err
}

func (b *MyConnBus) SendFrame(f MyFrame) {
	l := make([]byte, 2)
	binary.BigEndian.PutUint16(l, uint16(len(f)))
	b.Write(l)
	b.Write(f)
}

// // local bus
// // not used
// type MyReadWriteBus struct {
// 	io.Reader
// 	io.Writer

// 	sync.Mutex
// }

// func NewReaderWriterBus(reader io.Reader, writer io.Writer) *MyReadWriteBus {
// 	return &MyReadWriteBus{
// 		Reader: reader,
// 		Writer: writer,
// 	}
// }

// func (b *MyReadWriteBus) RecvFrame() (MyFrame, error) {
// 	f := make([]byte, 1500)
// 	n, err := b.Read(f)
// 	return MyFrame(f[:n]), err
// }

// func (b *MyReadWriteBus) SendFrame(f MyFrame) error {
// 	_, err := b.Write(f)
// 	return err
// }

type MyPipeBus struct {
	MyBusReader
	MyBusWriter

	// sync.Mutex // dont need this, it is in MyBusReader.

	closed bool
}

func (b *MyPipeBus) Close() error {
	if b.closed {
		return fmt.Errorf("my pipe bus already closed")
	}
	b.closed = true
	b.MyBusReader.Close()
	b.MyBusWriter.Close()
	return nil
}

func NewPipeBus(reader MyBusReader, writer MyBusWriter) *MyPipeBus {
	return &MyPipeBus{
		MyBusReader: reader,
		MyBusWriter: writer,
	}
}

func NewBusPipe() (*MyPipeBus, *MyPipeBus) {
	a2bReader, b2aWriter := NewPipe()
	b2aReader, a2bWriter := NewPipe()
	a2bBus := NewPipeBus(a2bReader, a2bWriter)
	b2aBus := NewPipeBus(b2aReader, b2aWriter)
	return a2bBus, b2aBus
}
