package echo

import (
	"github.com/Hana-ame/api-pack/Tools/debug"
	mymux "github.com/Hana-ame/api-pack/Tools/my_mux"
)

// not tested.
func Echo(b mymux.MyBus, receiveFrameDebuger, sendFrameDebuger func(mymux.MyFrame)) {
	const Tag = "Echo"
	for {
		rf, e := b.RecvFrame()
		if e != nil {
			debug.E(Tag, e.Error())
			continue
		}

		if receiveFrameDebuger != nil {
			receiveFrameDebuger(rf)
		}

		src, dst, cmd := rf.Source(), rf.Destination(), rf.Command()
		if cmd == mymux.Request {
			cmd = mymux.Accept
		}
		sf := mymux.NewFrame(dst, src, rf.Port(), cmd, rf.SequenceNumber(), rf.AcknowledgeNumber(), rf.Data())

		e = b.SendFrame(sf)
		if e != nil {
			debug.E(Tag, e.Error())
			continue
		}

		if sendFrameDebuger != nil {
			sendFrameDebuger(rf)
		}
	}
}
