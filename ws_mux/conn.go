package wsmux

import (
	"fmt"
	"io"
	"sync"

	"github.com/gorilla/websocket"
)

type WsConn struct {
	sync.Mutex

	*WsMux

	ID       uint16 // WsMux.SeqN
	SeqN     uint16
	ReadChan chan *WsPackage

	MTU int

	closed bool
}

func NewWsConn(id uint16, w *WsMux) *WsConn {
	conn := &WsConn{
		WsMux:    w,
		ID:       id,
		ReadChan: make(chan *WsPackage, 32),

		MTU: 1024,
	}

	return conn
}

func (c *WsConn) PutPackage(pkg *WsPackage) bool {
	select {
	case c.ReadChan <- pkg:
		return true
	default:
		return false
	}
}

func (c *WsConn) ReadPackage() *WsPackage {
	return <-c.ReadChan
}
func (c *WsConn) WritePackage(pkg *WsPackage) error {
	if c.closed {
		return fmt.Errorf("WsConn is closed")
	}

	if pkg == nil {
		pkg = &WsPackage{ID: c.ID, SeqN: c.SeqN, Message: []byte{}}
	}
	err := c.WriteMessage(websocket.BinaryMessage, pkg.ToBytes())

	return err
}

func (c *WsConn) Read(p []byte) (n int, err error) {
	pkg := c.ReadPackage()
	if len(pkg.Message) == 0 {
		err = io.EOF
		c.Close()
	}
	return copy(p, pkg.Message), err
}
func (c *WsConn) Write(p []byte) (n int, err error) {
	c.Lock()
	defer c.Unlock()
	pkg := &WsPackage{
		ID:      c.ID,
		SeqN:    c.SeqN,
		Message: p,
	}
	err = c.WritePackage(pkg)
	if err != nil {
		c.SeqN++
	}
	return len(pkg.Message), err
}

func (c *WsConn) Close() error {
	c.Lock()
	defer c.Unlock()

	if c.closed {
		return nil
	}
	c.WsMux.DeleteConn(c.ID)
	c.Write([]byte{})
	c.closed = true
	return nil
}
