package mymux

import "testing"

func TestBus(t *testing.T) {
	muxReader, busWriter := NewPipe()
	busReader, muxWriter := NewPipe()

	mux := NewMuxServer(muxWriter, 1)
	go mux.ReadDaemon(muxReader)

	bus := NewPipeBus(busReader, busWriter)

	router := NewRouter()
	_ = bus
	_ = mux
	_ = router
}
