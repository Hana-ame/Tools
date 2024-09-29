package mymux

import (
	"fmt"
	"sync"

	log "github.com/Hana-ame/udptun/Tools/debug"
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
	// PrintFrame(f) // debug
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

func NewDebugPipe() (MyBusReader, MyBusWriter) {
	pipeR := &MyPipe{Cond: sync.NewCond(&sync.Mutex{})}
	pipeW := &MyPipe{Cond: sync.NewCond(&sync.Mutex{})}
	go func() {
		for {
			f, e := pipeW.RecvFrame()
			if e != nil {
				log.E("debug pipe", e)
			} else if len(f) < FrameHeadLength {
				log.W("debug pipe", "length = ", len(f))
			} else {
				PrintFrame(f)
				e = pipeR.SendFrame(f)
				if e != nil {
					log.E("debug pipe", e)
				}
			}
		}
	}()
	return pipeR, pipeW
}
