package mymux

import (
	"io"
	"net"
)

type MyBus interface {
	MyBusReader
	MyBusWriter
}

type MyBusWriter interface {
	SendFrame(MyFrame) error
}

type MyBusReader interface {
	RecvFrame() (MyFrame, error)
	IsReading() bool
	SetReading(bool)
}

type MyConnBus struct {
	net.Conn
	reading bool
}

func (b *MyConnBus) IsReading() bool {
	return b.reading
}
func (b *MyConnBus) SetReading(reading bool) {
	b.reading = reading
}

func (b *MyConnBus) RecvFrame() (MyFrame, error) {
	f := make([]byte, 1500)
	n, err := b.Read(f)
	return MyFrame(f[:n]), err
}

func (b *MyConnBus) SendFrame(f MyFrame) {
	b.Write(f)
}

type MyReadWriteBus struct {
	io.Reader
	io.Writer
	reading bool
}

func NewReaderWriterBus(reader io.Reader, writer io.Writer) *MyReadWriteBus {
	return &MyReadWriteBus{
		Reader: reader,
		Writer: writer,
	}
}
func (b *MyReadWriteBus) IsReading() bool {
	return b.reading
}
func (b *MyReadWriteBus) SetReading(reading bool) {
	b.reading = reading
}

func (b *MyReadWriteBus) RecvFrame() (MyFrame, error) {
	f := make([]byte, 1500)
	n, err := b.Read(f)
	return MyFrame(f[:n]), err
}

func (b *MyReadWriteBus) SendFrame(f MyFrame) error {
	_, err := b.Write(f)
	return err
}
