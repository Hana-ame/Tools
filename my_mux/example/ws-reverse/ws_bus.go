package wsreverse

import (
	"sync"
	"time"

	"github.com/Hana-ame/udptun/Tools/debug"
	mymux "github.com/Hana-ame/udptun/Tools/my_mux"
	"github.com/gorilla/websocket"
)

// 会无限重试websocket.Conn
// 通过再loader中定义新Conn的生成方式
// 取代websocket.Conn的位置，表现为websocket.Conn

type ConnWriter struct {
	*websocket.Conn
	sync.Mutex
}

func (w *ConnWriter) WriteMessage(messageType int, data []byte) error {
	// const Tag = "ConnWriter.WriteMessage"
	w.Lock()
	defer w.Unlock()

	return w.Conn.WriteMessage(messageType, data)
}

type ConnReader struct {
	*websocket.Conn
	sync.Mutex
}

func (r *ConnReader) ReadMessage() (messageType int, data []byte, err error) {
	// const Tag = "ConnWriter.WriteMessage"
	r.Lock()
	defer r.Unlock()

	return r.Conn.ReadMessage()
}

// 带锁的websockt.Conn，不能同时写或者同时读
// 可以使用setConn重置
type Conn struct {
	*ConnReader
	*ConnWriter

	// accept or connect ws
	// loader func() *websocket.Conn

	*sync.Cond

	onError bool
	closed  bool
}

func NewConn(c *websocket.Conn) *Conn {
	return &Conn{
		ConnReader: &ConnReader{Conn: c},
		ConnWriter: &ConnWriter{Conn: c},
		Cond:       sync.NewCond(&sync.Mutex{}),
	}
}

// 大概有问题。
func (c *Conn) WaitOnError() {
	c.L.Lock()
	c.onError = true
	for c.onError {
		c.Wait()
	}
	c.L.Unlock()
}

func (c *Conn) SetConn(conn *websocket.Conn) {
	c.L.Lock()

	c.ConnWriter.Conn.Close()
	c.ConnReader.Conn.Close()

	c.ConnReader = &ConnReader{Conn: conn}
	c.ConnWriter = &ConnWriter{Conn: conn}

	c.onError = false

	c.L.Unlock()
	c.Broadcast()
}

func (c *Conn) Close() {
	c.closed = true

	c.ConnWriter.Conn.Close()
	c.ConnReader.Conn.Close()
}

// [0, id]  接收前
// [data]
// [1，id]  这个是response

const (
	CLIENT_RECV_SHOULD_BE_ID = iota
	CLIENT_RECV_SHOULD_BE_DATA
)

func NewWsClient(dst string, timeout time.Duration) mymux.MyBus {
	const Tag = "NewWsClient"
	// cbus will return to client mux to use
	cbus, sbus := mymux.NewPipeBusPair()

	dialer := func() *websocket.Conn {
		// 	const Tag = "dialer"
		for {
			conn, _, err := websocket.DefaultDialer.Dial(dst, nil)
			if err == nil {
				return conn
			}
			debug.E(Tag, err.Error())
		}
	}
	// create conn from websocket.conn
	conn := NewConn(dialer())

	var size uint8 = 64
	buffer := mymux.NewGBNBuffer(uint8(size))

	// onerr := false

	// read channel
	go func() {
		const Tag = "client read channel"
		var next uint8 = 0
		var nextState = CLIENT_RECV_SHOULD_BE_ID
	loop:
		for {
			msgType, data, err := conn.ReadMessage()
			if err != nil {
				debug.E(Tag, err.Error())
				conn.SetConn(dialer())
				continue
			}
			switch msgType {
			case websocket.TextMessage:
				switch data[0] {
				case 1: // it is a acknowledge
					buffer.SetRead(data[1]) // should be moded by size
					buffer.SetTail(data[1]) // should be moded by size
				case 0: //
					if nextState != CLIENT_RECV_SHOULD_BE_ID {
						conn.WriteMessage(websocket.TextMessage, []byte{1, next})
						nextState = CLIENT_RECV_SHOULD_BE_ID
						continue loop
					}
					if next != data[1] {
						conn.WriteMessage(websocket.TextMessage, []byte{1, next})
						nextState = CLIENT_RECV_SHOULD_BE_ID
						continue loop
					}
					nextState = CLIENT_RECV_SHOULD_BE_DATA
				}
			case websocket.BinaryMessage:
				if nextState != CLIENT_RECV_SHOULD_BE_DATA {
					conn.WriteMessage(websocket.TextMessage, []byte{1, next})
					nextState = CLIENT_RECV_SHOULD_BE_ID
					continue loop
				}
				e := sbus.SendFrame(data)
				if e != nil {
					debug.E(Tag, e.Error())
					continue
				}

				nextState = CLIENT_RECV_SHOULD_BE_ID
				next++

				conn.WriteMessage(websocket.TextMessage, []byte{1, next})
			}
		}
	}()

	// write channel
	// bus side
	go func() {
		const Tag = "client write channel bus side"
		for {
			f, e := sbus.RecvFrame()
			if e != nil {
				debug.E(Tag, e.Error())
				continue
			}

			buffer.Offer(f)
		}
	}()

	// conn side
	go func() {
		const Tag = "client write channel bus side"
		for {
			id, data, e := buffer.Read()
			if !e {
				debug.E(Tag, id, data, "not existed")
			}
			conn.WriteMessage(websocket.TextMessage, []byte{0, id})
			conn.WriteMessage(websocket.BinaryMessage, data)
		}
	}()

	return cbus
}

func NewWsServer(conn *Conn) mymux.MyBus {
	const Tag = "NewWsServer"
	// cbus will return to client mux to use
	cbus, sbus := mymux.NewPipeBusPair()

	var size uint8 = 64
	buffer := mymux.NewGBNBuffer(uint8(size))

	// read channel
	go func() {
		const Tag = "server read channel"
		var next uint8 = 0
		var nextState = CLIENT_RECV_SHOULD_BE_ID
	loop:
		for {
			msgType, data, err := conn.ReadMessage()
			if err != nil {
				debug.E(Tag, err.Error())
				conn.WaitOnError()
				continue
			}
			switch msgType {
			case websocket.TextMessage:
				switch data[0] {
				case 1: // it is a acknowledge
					buffer.SetRead(data[1]) // should be moded by size
					buffer.SetTail(data[1]) // should be moded by size
				case 0: //
					if nextState != CLIENT_RECV_SHOULD_BE_ID {
						conn.WriteMessage(websocket.TextMessage, []byte{1, next})
						nextState = CLIENT_RECV_SHOULD_BE_ID
						continue loop
					}
					if next != data[1] {
						conn.WriteMessage(websocket.TextMessage, []byte{1, next})
						nextState = CLIENT_RECV_SHOULD_BE_ID
						continue loop
					}
					nextState = CLIENT_RECV_SHOULD_BE_DATA
				}
			case websocket.BinaryMessage:
				if nextState != CLIENT_RECV_SHOULD_BE_DATA {
					conn.WriteMessage(websocket.TextMessage, []byte{1, next})
					nextState = CLIENT_RECV_SHOULD_BE_ID
					continue loop
				}
				e := sbus.SendFrame(data)
				if e != nil {
					debug.E(Tag, e.Error())
					continue
				}

				nextState = CLIENT_RECV_SHOULD_BE_ID
				next++

				conn.WriteMessage(websocket.TextMessage, []byte{1, next})
			}
		}
	}()

	// write channel
	// bus side
	go func() {
		const Tag = "client write channel bus side"
		for {
			f, e := sbus.RecvFrame()
			if e != nil {
				debug.E(Tag, e.Error())
				continue
			}

			buffer.Offer(f)
		}
	}()

	// conn side
	go func() {
		const Tag = "client write channel bus side"
		for {
			id, data, e := buffer.Read()
			if !e {
				debug.E(Tag, id, data, "not existed")
			}
			conn.WriteMessage(websocket.TextMessage, []byte{0, id})
			conn.WriteMessage(websocket.BinaryMessage, data)
		}
	}()

	return cbus
}
