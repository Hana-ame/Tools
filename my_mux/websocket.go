package mymux

import (
	"github.com/gorilla/websocket"
)

type WebSocketNode struct {
	reading bool
	writing bool
	Conn    *websocket.Conn
	Node    // 假设 Node 是一个定义好的接口或结构体
}

func (n *WebSocketNode) SetConn(c *websocket.Conn) {
	n.Conn = c
}

func (n *WebSocketNode) SetReading(f bool) {
	n.reading = f
}

func (n *WebSocketNode) SetWriting(f bool) {
	n.writing = f
}

func (n *WebSocketNode) ReadCopy() error {
	defer n.SetReading(false)
	n.reading = true
	for n.reading {
		_, p, err := n.Conn.ReadMessage()
		if err != nil {
			return err
		}
		err = n.SendFrame(p)
		if err != nil {
			return err
		}
	}
	return nil
}

func (n *WebSocketNode) WriteCopy() error {
	defer n.SetWriting(false)
	n.writing = true
	for n.writing {
		f, err := n.RecvFrame()
		if err != nil {
			return err
		}
		err = n.Conn.WriteMessage(websocket.BinaryMessage, f)
		if err != nil {
			return err
		}
	}
	return nil
}
