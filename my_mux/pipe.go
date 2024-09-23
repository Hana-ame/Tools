package mymux

import (
	"fmt"
	"sync"
)

const (
	ERR_PIPE_CLOSED = "my pipe closed"
)

// not tested
type MyPipe struct {
	// ch chan MyFrame
	*sync.Cond

	sync.Mutex // for only one read deamon

	f MyFrame

	closed bool
}

func (p *MyPipe) SendFrame(f MyFrame) (err error) {
	p.L.Lock()
	for p.f != nil && !p.closed {
		p.Wait()
	}
	if p.closed {
		err = fmt.Errorf(ERR_PIPE_CLOSED)
	}
	p.f = f
	p.L.Unlock()

	p.Signal()
	return
}

func (p *MyPipe) RecvFrame() (f MyFrame, err error) {
	p.L.Lock()
	for p.f == nil && !p.closed {
		p.Wait()
	}

	if p.closed {
		err = fmt.Errorf(ERR_PIPE_CLOSED)
	}
	f = p.f
	p.f = nil
	p.L.Unlock()

	p.Signal()
	PrintFrame(f) // debug/
	return f, err
}

func (p *MyPipe) Close() error {
	p.closed = true
	p.Broadcast()
	return nil
}

func NewPipe() (MyBusReader, MyBusWriter) {
	pipe := &MyPipe{Cond: sync.NewCond(&sync.Mutex{})}
	return pipe, pipe
}
