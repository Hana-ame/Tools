package mymux

import (
	"fmt"

	tools "github.com/hana-ame/udptun/Tools"
)

type FrameTag [6]byte

func (f FrameTag) Tag() FrameTag {
	return f
}

type MyMux interface {
	MyBusWriter

	RemoveConn(*MyConn)
}

type MyMuxServer struct {
	MyBusWriter

	localAddr Addr

	// SequenceNumber uint8 // for control frame
	*tools.ConcurrentHashMap[FrameTag, *MyConn]
	acceptedConnChannel chan *MyConn
}

func NewMuxServer(writer MyBusWriter) *MyMuxServer {
	mux := &MyMuxServer{
		MyBusWriter: writer,

		ConcurrentHashMap:   tools.NewConcurrentHashMap[FrameTag, *MyConn](),
		acceptedConnChannel: make(chan *MyConn),
	}
	return mux
}

func (m *MyMuxServer) RemoveConn(c *MyConn) {
	m.Remove(c.Tag())
}

func (m *MyMuxServer) Accept() *MyConn {
	return <-m.acceptedConnChannel
}

func (m *MyMuxServer) ReadDaemon(c MyBusReader) {
	if c.IsReading() {
		return
	}
	c.SetReading(true)
	defer c.SetReading(false)

	for {
		f, _ := c.RecvFrame()
		switch f.Command() {
		case Request:
			// 创建新Conn
			if _, exist := m.Get(f.Tag()); !exist {
				newConn := NewConn(m, f.Tag(), f.Destination(), f.Source(), f.Port()) // 会反一下
				m.Put(newConn.Tag(), newConn)
				m.acceptedConnChannel <- newConn
			}
			m.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Acknowledge, 0, 0))
		case Acknowledge:
			continue

		default:
			// 其他情况直接转发
			if conn, exist := m.Get(f.Tag()); exist {
				conn.PutFrame(f)
			} else {
				// not exist
				if f.Command() == Close {
					// if the command is close, not return another close
					continue
				}
				m.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
			}
		}
	}

}

type MyMuxClient struct {
	MyBusWriter

	localAddr Addr
	// SequenceNumber uint8 // for control frame
	*tools.ConcurrentHashMap[FrameTag, *MyConn]

	nextport uint8
}

func NewMuxClient(writer MyBusWriter) *MyMuxClient {
	mux := &MyMuxClient{
		MyBusWriter: writer,

		ConcurrentHashMap: tools.NewConcurrentHashMap[FrameTag, *MyConn](),
	}
	return mux
}

func (m *MyMuxClient) RemoveConn(c *MyConn) {
	m.Remove(c.Tag())
}

func (m *MyMuxClient) Dial(dst Addr) (*MyConn, error) {
	if m.Size() > 254 {
		return nil, fmt.Errorf("no other ports")
	}
	f := NewCtrlFrame(m.localAddr, dst, m.nextport, Request, 0, 0)
	// 留出 port 0
	for m.Contains(f.Tag()) || m.nextport == 0 {
		m.nextport++
		f.SetPort(m.nextport)
	}
	c := NewConn(m, f.Tag(), m.localAddr, dst, m.nextport)

	// 请求建立链接
	m.SendFrame(f)
	m.PutIfAbsent(c.Tag(), c)

	m.nextport++

	return c, nil
}

func (m *MyMuxClient) ReadDaemon(c MyBusReader) {
	if c.IsReading() {
		return
	}
	c.SetReading(true)
	defer c.SetReading(false)

	for {
		f, _ := c.RecvFrame()
		switch f.Command() {
		case Request:
			// 不会有的，拒绝链接
			m.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
			continue
		case Acknowledge:
			continue
		default:
			// 其他情况直接转发
			if conn, exist := m.Get(f.Tag()); exist {
				conn.PutFrame(f)
			} else {
				// not exist
				if f.Command() == Close {
					// if the command is close, not return another close
					continue
				}
				m.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
			}
		}
	}

}
