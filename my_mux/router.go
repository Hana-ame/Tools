package mymux

import (
	"fmt"
	"sync"

	tools "github.com/hana-ame/udptun/Tools"
)

// not tested
type MyPipe struct {
	// ch chan MyFrame
	sync.Cond
	f      MyFrame
	closed bool

	reading bool
}

func (p *MyPipe) SetReading(reading bool) {
	p.reading = reading
}
func (p *MyPipe) IsReading() bool {
	return p.reading
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

func NewPipe() (MyBusReader, MyBusWriter) {
	pipe := &MyPipe{}
	return pipe, pipe
}

// TODO
type MyRoute struct {
	*tools.ConcurrentHashMap[uint16, *MyBus]
}

func NewRouter() *MyRoute {
	router := &MyRoute{
		ConcurrentHashMap: tools.NewConcurrentHashMap[uint16, *MyBus](),
		// buses: make([]*MyBus, 25),
	}
	return router
}

// func (r *MyRoute) ReadDaemon(b *MyBus) {
// 	for {
// 		f, err := b.RecvFrame()
// 		if err != nil {
// 			log.Println(err)
// 		}
// 		// 怎么处理草泥马
// 	}
// }
