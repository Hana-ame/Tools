package wsreverse

import (
	"sync"

	"github.com/gorilla/websocket"
)

// 会无限重试websocket.Conn
// 通过再loader中定义新Conn的生成方式
// 取代websocket.Conn的位置，表现为websocket.Conn
type Conn struct {
	*websocket.Conn

	// accept or connect ws
	// loader func() *websocket.Conn

	sync.Mutex

	closed bool
}

func (c *Conn) Close() {
	c.closed = true
	c.Conn.Close()
}

func (c *Conn) SetConn(conn *websocket.Conn) {
	c.Lock()
	defer c.Unlock()

	c.Conn.Close()
	c.Conn = conn
}

func (c *Conn) WriteMessage(messageType int, data []byte) error {
	const Tag = "Conn.WriteMessage"
	c.Lock()
	defer c.Unlock()

	return c.Conn.WriteMessage(messageType, data)
}

func (c *Conn) ReadMessage() (int, []byte, error) {
	const Tag = "Conn.ReadMessage"
	c.Lock()
	defer c.Unlock()

	return c.Conn.ReadMessage()
}

type record struct {
	id   uint8
	data []byte
}

// buffer

// window no larger than 127
type Buffer struct {
	size uint8

	buffer []*record
	valid  []bool

	head uint8
	tail uint8

	sync.Cond
	closed bool
}

func NewBuffer(size uint8) *Buffer {
	buf := &Buffer{
		size:   size,
		buffer: make([]*record, size),
		valid:  make([]bool, size),
		Cond:   *sync.NewCond(&sync.Mutex{}),
	}
	return buf
}

func (b *Buffer) Offer(data []byte) {
	b.L.Lock()
	// 有效 且 not closed 时 等待
	for (b.valid[b.head%b.size]) && !b.closed {
		b.Wait()
	}
	b.buffer[b.head%b.size] = &record{(b.head), data}
	b.valid[b.head%b.size] = true
	b.head++
	b.L.Unlock()
	b.Broadcast()
}

func (b *Buffer) Read(id uint8) (uint8, []byte, bool) {
	// b.L.Lock()
	// 无效 且 not closed 时 等待
	// for (!b.valid[id%b.size]) && !b.closed {
	// b.Wait()
	// }
	record, ok := b.buffer[id%b.size], b.valid[id%b.size]
	// b.L.Unlock()
	// b.Broadcast()
	return record.id, record.data, ok

}

// func (b *MyBuffer) Remove(id uint8) {
// 	b.L.Lock()
// 	b.valid[id%b.size] = false
// 	for !b.valid[b.tail%b.size] {
// 		b.tail++
// 	}
// 	b.L.Unlock()
// 	b.Broadcast()
// }

func (b *Buffer) SetTail(tail uint8) {
	b.L.Lock()
	for tail-b.tail > 0 {
		b.valid[b.tail%b.size] = false
		b.tail++
	}
	b.L.Unlock()
	b.Broadcast()
}

// // 接续在Conn上，
// type WsBus struct {
// 	*Conn

// 	// SendFrame -> WriteMessage
// 	writebuf mymux.MyBuffer

// 	sync.Mutex
// }

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
