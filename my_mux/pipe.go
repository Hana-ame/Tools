package mymux

import (
	"fmt"
	"sync"
)

// not tested
type MyPipe struct {
	// ch chan MyFrame
	sync.Cond

	sync.Mutex // for only one read deamon

	f MyFrame

	closed bool
}

func (p *MyPipe) SendFrame(f MyFrame) error {
	for p.f != nil || !p.closed {
		p.Wait()
	}
	if p.closed {
		return fmt.Errorf("closed")
	}
	p.f = f

	p.Signal()
	return nil
}

func (p *MyPipe) RecvFrame() (MyFrame, error) {
	for p.f == nil && !p.closed {
		p.Wait()
	}
	if p.closed {
		return nil, fmt.Errorf("closed")
	}
	f := p.f
	p.f = nil

	p.Signal()
	return f, nil
}

func (p *MyPipe) Close() error {
	p.closed = true
	p.Broadcast()
	return nil
}

func NewPipe() (MyBusReader, MyBusWriter) {
	pipe := &MyPipe{}
	return pipe, pipe
}
