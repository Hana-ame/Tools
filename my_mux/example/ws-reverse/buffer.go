package wsreverse

import "sync"

// buffer

// window no larger than 127
type Buffer struct {
	size uint8

	buffer []*record
	valid  []bool

	head uint8
	tail uint8
	rptr uint8

	*sync.Cond

	closed bool
}

func NewBuffer(size uint8) *Buffer {
	buf := &Buffer{
		size:   size,
		buffer: make([]*record, size),
		valid:  make([]bool, size),
		Cond:   sync.NewCond(&sync.Mutex{}),
	}
	return buf
}

func (b *Buffer) Offer(data []byte) {
	b.L.Lock()
	// 有效 且 未closed 时等待
	for (b.valid[b.head%b.size]) && !b.closed {
		b.Wait()
	}
	b.buffer[b.head%b.size] = &record{(b.head), data}
	b.valid[b.head%b.size] = true
	b.head++
	b.L.Unlock()
	b.Broadcast()
}

func (b *Buffer) Read() (uint8, []byte, bool) {
	b.L.Lock()
	// 无效 且 可以读取(即rptr小于head) 且 未closed 时等待
	for ((!b.valid[b.rptr%b.size]) || (b.rptr == b.head)) && !b.closed {
		b.Wait()
	}
	record, ok := b.buffer[b.rptr%b.size], b.valid[b.rptr%b.size]
	b.rptr++
	b.L.Unlock()
	b.Broadcast()
	return record.id, record.data, ok

}

func (b *Buffer) SetTail(tail uint8) {
	b.L.Lock()
	for tail-b.tail > 0 {
		b.valid[b.tail%b.size] = false
		b.tail++
	}
	b.L.Unlock()
	b.Broadcast()
}

func (b *Buffer) SetReadPtr(rptr uint8) {
	b.L.Lock()
	b.rptr = rptr
	b.L.Unlock()
	b.Broadcast()
}

func (b *Buffer) Close() {
	b.L.Lock()
	b.closed = true
	b.L.Unlock()
	b.Broadcast()
}
