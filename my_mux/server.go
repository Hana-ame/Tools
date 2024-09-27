package mymux

import tools "github.com/Hana-ame/neo-moonchan/Tools"

type MyServer struct {
	MyBus

	localAddr Addr
	*tools.ConcurrentHashMap[MyTag, MyBus]

	accpetChannel chan *MyFrameConn
}

func NewServer(bus MyBus, addr Addr) *MyServer {
	server := &MyServer{
		MyBus:             bus,
		localAddr:         addr,
		ConcurrentHashMap: tools.NewConcurrentHashMap[MyTag, MyBus](),

		accpetChannel: make(chan *MyFrameConn, 5),
	}
	return server
}
func (s *MyServer) ReadDeamon() error {
	s.Lock()
	defer s.Unlock()
	for {
		f, err := s.RecvFrame()
		if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
			s.Close()
			return err
		}
		switch f.Command() {
		case Request:
			// 不响应不是叫自己的
			if s.localAddr != 0 && f.Destination() != s.localAddr {
				continue
			}
			// 创建新Conn
			if _, exist := s.Get(f.Tag()); !exist {
				cBus, sBus := NewPipeBusPair()
				go func(b MyBus, tag MyTag) {
					// bus对面是client conn
					for {
						f, err := b.RecvFrame()
						if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
							s.Remove(tag)
						}
						s.SendFrame(f)
					}
				}(sBus, f.Tag())
				c := NewFrameConn(cBus, f.Destination(), f.Source(), f.Port()) // 会反一下
				s.Put(f.Tag(), sBus)
				s.accpetChannel <- c
				s.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Accept, 0, 0))
			}
		default:
			// 其他情况直接转发
			if b, exist := s.Get(f.Tag()); exist {
				b.SendFrame(f)
			} else {
				if f.Command() == Close {
					continue
				}
				s.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
			}
		}
	}
}

func (s *MyServer) Accpet() *MyFrameConn {
	return <-s.accpetChannel
}
