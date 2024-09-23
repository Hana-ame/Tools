package mymux

import (
	tools "github.com/hana-ame/udptun/Tools"
)

type portMap [32]byte

func (m *portMap) ContainsPort(i uint8) bool {
	return 0 != m[i/8]&(1<<(i%8))
}
func (m *portMap) SetPort(i uint8) {
	m[i/8] |= (1 << (i % 8))
}
func (m *portMap) RemovePort(i uint8) {
	m[i/8] &= ^(1 << (i % 8))
}

func NewClientFrameConn(bus MyBus, remote, local Addr, port uint8) *MyFrameConn {
	bus.SendFrame(NewCtrlFrame(local, remote, port, Request, 0, 0))
	return NewFrameConn(bus, local, remote, port)
}

type Client struct {
	MyBus

	localAddr Addr

	*tools.ConcurrentHashMap[MyTag, MyBus]

	*portMap
	nextport uint8
}

func NewClient(bus MyBus, localAddr Addr) *Client {
	client := &Client{
		MyBus: bus,

		localAddr: localAddr,

		ConcurrentHashMap: tools.NewConcurrentHashMap[MyTag, MyBus](),
		portMap:           &portMap{},
	}
	return client
}

func (c *Client) ReadDaemon() error {
	c.Lock()
	defer c.Unlock()

	for {
		f, err := c.RecvFrame()
		if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
			c.Close()
			return err
		}
		switch f.Command() {
		case Request:
			c.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
		default:
			// 其他情况直接转发
			if b, exist := c.Get(f.Tag()); exist {
				b.SendFrame(f)
			} else {
				if f.Command() == Close {
					continue
				}
				c.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
			}
		}
	}
}

func (s *Client) Dial(dst Addr) (*MyFrameConn, error) {

	for s.ContainsPort(s.nextport) {
		s.nextport++
	}
	cBus, sBus := NewBusPipe()
	go func(b MyBus, tag MyTag, port uint8) {
		// bus对面是client conn
		for {
			f, err := b.RecvFrame()
			if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
				s.Remove(tag)
				s.RemovePort(port)
			}
			err = s.SendFrame(f)
			if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
				s.Remove(tag)
				s.RemovePort(port)
			}
		}
	}(sBus, NewTag(dst, s.localAddr, s.nextport), s.nextport)
	c := NewClientFrameConn(cBus, s.localAddr, dst, s.nextport)

	// // debug
	// log.Println("mapmapmap after dial")
	// m.PrintMap()

	s.nextport++

	return c, nil
}
