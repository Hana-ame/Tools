// not tested.

package mymux

import (
	"sync"
)

// window no larger than 127
type MyBuffer struct {
	size   uint8
	buffer [][]byte
	valid  []bool

	head uint8
	tail uint8

	sync.Cond
	closed bool
}

func NewBuffer(size uint8) *MyBuffer {
	buf := &MyBuffer{
		size:   size,
		buffer: make([][]byte, size),
		valid:  make([]bool, size),
	}
	return buf
}

func (b *MyBuffer) IsEmpty() bool {
	return b.head == b.tail
}
func (b *MyBuffer) IsFull() bool {
	return b.head-b.tail == b.size
}

func (b *MyBuffer) Offer(data []byte) {
	for (b.valid[b.head]) && !b.closed {
		b.Wait()
	}
	b.buffer[b.head] = data
	b.valid[b.head] = true
	b.head++
	b.Broadcast()
}
func (b *MyBuffer) Poll() []byte {
	for !(b.valid[b.tail]) && !b.closed {
		b.Wait()
	}
	data := b.buffer[b.tail]
	b.valid[b.tail] = false
	b.tail++
	b.Broadcast()
	return data
}

func (b *MyBuffer) SetTail(tail uint8) {
	for b.tail < tail {
		b.valid[b.tail] = false
		b.tail++
	}

	// b.head = tail + b.size
	b.Broadcast()
}

// func (b *MyBuffer) SetHead(head uint8) {
// 	b.head = head
// 	b.tail = head - b.size
// 	b.Broadcast()
// }

func (b *MyBuffer) Put(p uint8, data []byte) {
	for !(p-b.tail < b.size && !b.valid[p%b.size]) && !b.closed {
		b.Wait()
	}
	b.buffer[p%b.size] = data
	b.valid[p%b.size] = true
	b.Broadcast()
}
func (b *MyBuffer) Get(p uint8) []byte {
	for !(p-b.tail < b.size && b.valid[p%b.size]) && !b.closed {
		b.Wait()
	}
	data := b.buffer[p%b.size]
	b.Broadcast()
	return data
}

func (b *MyBuffer) Close() {
	b.closed = true
	b.Broadcast()
}
