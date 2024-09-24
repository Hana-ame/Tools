package mymux

import (
	"fmt"
	"testing"
)

func TestMutex(t *testing.T) {
	reader, writer := NewPipe()
	bus := NewBusFromPipe(reader, writer)
	reader.Lock()
	bus.Lock()
	fmt.Println("never")
}
