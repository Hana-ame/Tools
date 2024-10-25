package mymux

import "github.com/Hana-ame/udptun/Tools/debug"

type Helper string

func (h Helper) ReadBus(r BusReader) {
	for {
		f, e := r.RecvFrame()
		if e != nil {
			debug.W(h, e)
		}
		debug.I(h, (f).String())
	}
}
