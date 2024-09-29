package mymux

import "testing"

// not tested.
func TestBus(t *testing.T) {
	muxReader, busWriter := NewPipe()
	busReader, muxWriter := NewPipe()

	mux := NewMuxServer(muxWriter, 1)
	go mux.ReadDaemon(muxReader)

	bus := NewBusFromPipe(busReader, busWriter)

	router := NewRouter()
	_ = bus
	_ = mux
	_ = router
}
