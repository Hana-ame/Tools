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
	const Tag = "ConnWriter.WriteMessage"
	w.Lock()
	defer w.Unlock()

	return w.Conn.WriteMessage(messageType, data)
}

type ConnReader struct {
	*websocket.Conn
	sync.Mutex
}

func (r *ConnReader) ReadMessage() (messageType int, data []byte, err error) {
	const Tag = "ConnWriter.WriteMessage"
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

	sync.Mutex

	closed bool
}

func NewConn(c *websocket.Conn) *Conn {
	return &Conn{
		ConnReader: &ConnReader{Conn: c},
		ConnWriter: &ConnWriter{Conn: c},
	}
}

func (c *Conn) SetConn(conn *websocket.Conn) {
	// c.Lock()
	// defer c.Unlock()

	c.ConnWriter.Conn.Close()
	c.ConnReader.Conn.Close()

	c.ConnReader = &ConnReader{Conn: conn}
	c.ConnWriter = &ConnWriter{Conn: conn}
}

// func (c *Conn) WriteMessage(messageType int, data []byte) error {
// 	const Tag = "Conn.WriteMessage"
// 	// c.Lock()
// 	// defer c.Unlock()

// 	return c.Conn.WriteMessage(messageType, data)
// }

// func (c *Conn) ReadMessage() (int, []byte, error) {
// 	const Tag = "Conn.ReadMessage"
// 	c.Lock()
// 	defer c.Unlock()

// 	return c.Conn.ReadMessage()
// }

func (c *Conn) Close() {
	c.closed = true

	c.ConnWriter.Conn.Close()
	c.ConnReader.Conn.Close()
}

type record struct {
	id   uint8
	data []byte
}

// // // 接续在Conn上，
// type WsBus struct {
// 	*Conn

// 	// reading channel
// 	nextReadId uint8

// 	// writing channel
// 	nextWriteId uint8 // this can be reset by nextReadId from remote
// 	*Buffer           // SendFrame -> WriteMessage

// 	sync.Cond
// 	onError bool

// 	receivingId    uint8
// 	receivingValid bool
// }

// func NewWsBus(c *Conn, buffer *Buffer) *WsBus {
// 	wsbus := &WsBus{
// 		Conn:   c,
// 		Buffer: buffer,
// 		Cond:   *sync.NewCond(&sync.Mutex{}),
// 	}
// 	return wsbus
// }

// func (b *WsBus) ReadDeamon() {
// 	for {
// 		msgType, data, err := b.ReadMessage()
// 		if err != nil {
// 			b.L.Lock()
// 			b.onError = true
// 			for b.onError {
// 				b.Wait()
// 			}
// 			b.L.Unlock()
// 			continue
// 		}
// 		switch msgType {
// 		case websocket.TextMessage: // control
// 			if data[0] == 0 { // data[0] = "next is data", data[1] = the next frame's id
// 				b.receivingId = data[1]
// 				b.receivingValid = true
// 			}
// 		case websocket.BinaryMessage: // data
// 			if b.receivingValid {
// 				b.receivingValid = false
// 			}
// 		}
// 	}
// }

// [0, id]  接收前
// [data]
// [1，id]  这个是response

const (
	CLIENT_RECV_SHOULD_BE_ID = iota
	CLIENT_RECV_SHOULD_BE_DATA
)

func NewWsClient(dst string, timeout time.Duration) mymux.MyBus {
	const Tag = "NewWsClient"
	cbus, sbus := mymux.NewPipeBusPair()

	dialer := func() *websocket.Conn {
		const Tag = "dialer"
		for {
			wsConn, _, err := websocket.DefaultDialer.Dial(dst, nil)
			if err == nil {
				return wsConn
			}
			debug.E(Tag, err.Error())
		}
	}
	// create conn from websocket.conn
	conn := NewConn(dialer())

	var size uint8 = 64
	buffer := NewBuffer(uint8(size))

	// read channel
	go func() {
		const Tag = "client read channel"
		var next uint8 = 0
		var nextState = CLIENT_RECV_SHOULD_BE_ID
	loop:
		for {
			msgType, data, err := conn.ReadMessage()
			if err != nil {
				conn.SetConn(dialer())
				continue
			}
			switch msgType {
			case websocket.TextMessage:
				switch data[0] {
				case 1: // it is a acknowledge
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
				}
			}
		}
	}()

	// write channel
	// go func() {
	// 	const Tag = "client write channel"
	// 	var next uint8 = 0
	// loop:
	// 	for {
	// 		f, e := sbus.RecvFrame()
	// 		t
	// 		if e != nil {
	// 			debug.E(Tag, e.Error())
	// 			continue loop
	// 		}
	// 	}
	// }()

	return cbus
}

// // 守护进程。
// func (b *WsBus) Deamon() {
// }

// func (b *WsBus) SendFrame(f *mymux.MyFrame) error {
// 	messageType, data := b.Conn.ReadMessage()
// 	if messageType == websocket.BinaryMessage {
// 		b.Conn.WriteMessage(websocket.TextMessage)
// 		return
// 	} else if messageType == websocket.TextMessage {
// 		// 回报接受到了

// 	}
// }

// // MyWsBus 用于 WebSocket 连接的总线结构。
// type MyWsBus struct {
// 	*websocket.Conn

// 	sync.Mutex // 仅允许一个读取守护进程读取。
// }

// // RecvFrame 从 WebSocket 连接接收一帧数据。
// func (b *MyWsBus) RecvFrame() (mymux.MyFrame, error) {
// 	_, f, err := b.ReadMessage()
// 	return mymux.MyFrame(f), err
// }

// // SendFrame 通过 WebSocket 发送一帧数据，并实现重传机制。
// func (b *MyWsBus) SendFrame(f mymux.MyFrame) error {
// 	const maxRetries = 3
// 	var err error

// 	for i := 0; i < maxRetries; i++ {
// 		err = b.WriteMessage(websocket.BinaryMessage, f)
// 		if err == nil {
// 			return nil // 成功发送，返回 nil
// 		}

// 		// 打印错误信息并等待一段时间重试
// 		time.Sleep(time.Second) // 可以根据需要调整重试间隔
// 	}

// 	return err // 返回最后一次的错误
// }
