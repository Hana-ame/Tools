package mymux

import (
	"sync"

	"github.com/gorilla/websocket"
)

func Websocket(wc *websocket.Conn, node Node) error {
	var err error
	cond := sync.NewCond(&sync.Mutex{})
	go func() {
		err = WebsocketReadCopy(wc, node)
		cond.Signal()
	}()
	go func() {
		err = WebsocketWriteCopy(wc, node)
		cond.Signal()
	}()

	cond.Wait()
	wc.Close()

	return err
}

func WebsocketReadCopy(wc *websocket.Conn, node Node) error {
	for {
		_, p, err := wc.ReadMessage()
		if err != nil {
			return err
		}
		err = node.SendFrame(p)
		if err != nil {
			return err
		}
	}
}
func WebsocketWriteCopy(wc *websocket.Conn, node Node) error {
	for {
		f, err := node.RecvFrame()
		if err != nil {
			return err
		}
		err = wc.WriteMessage(websocket.BinaryMessage, f)
		if err != nil {
			return err
		}
	}
}
