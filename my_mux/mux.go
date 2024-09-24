// 只能适配MyConn了，
// 大概会弃用

package mymux

import (
	"encoding/binary"
	"fmt"
	"log"
	"sync"

	tools "github.com/hana-ame/udptun/Tools"
)

const TagLength = 5

type MyTag [TagLength]byte

func NewTag(remoteAddr, localAddr Addr, port uint8) MyTag {
	var tag MyTag
	binary.BigEndian.PutUint16(tag[0:2], uint16(remoteAddr))
	binary.BigEndian.PutUint16(tag[2:4], uint16(localAddr))
	tag[4] = port
	return tag
}

func (f MyTag) Tag() MyTag {
	return f
}

type MyMux interface {
	MyBus

	RemoveConn(*MyConn)
}

type MyMuxServer struct {
	MyBusWriter

	localAddr Addr

	// SequenceNumber uint8 // for control frame
	*tools.ConcurrentHashMap[MyTag, *MyConn]
	acceptedConnChannel chan *MyConn
}

func NewMuxServer(writer MyBusWriter, localAddr Addr) *MyMuxServer {
	mux := &MyMuxServer{
		MyBusWriter: writer,

		localAddr: localAddr,

		ConcurrentHashMap:   tools.NewConcurrentHashMap[MyTag, *MyConn](),
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
	c.Lock()
	defer c.Unlock()

	for {
		f, _ := c.RecvFrame()
		// log.Println("!!s", f) // debug
		switch f.Command() {
		case Request:
			// 不响应不是叫自己的
			if f.Destination() != m.localAddr {
				continue
			}
			// 创建新Conn
			if _, exist := m.Get(f.Tag()); !exist {
				cBus, _ := NewPipeBusPair()
				c := NewConn(cBus, f.Tag(), f.Destination(), f.Source(), f.Port()) // 会反一下
				m.Put(c.Tag(), c)
				m.acceptedConnChannel <- c
			}
			m.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Accept, 0, 0))

			// // debug
			// log.Println("mapmapmap after request")
			// m.PrintMap() // debug

		case Accept:
			continue

		default:
			// 其他情况直接转发
			if conn, exist := m.Get(f.Tag()); exist {
				conn.PutFrame(f)
			} else {

				// // debug
				// log.Println("mapmapmap not exist")
				// m.PrintMap() // debug
				// log.Println(f.Tag())

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

func (m *MyMuxServer) PrintMap() {
	log.Println("print mux map", m.localAddr)
	m.ConcurrentHashMap.ForEach(func(key MyTag, value *MyConn) {
		fmt.Println(key, value)
	})
}

type MyMuxClient struct {
	MyBusWriter

	sync.Mutex

	localAddr Addr
	// SequenceNumber uint8 // for control frame
	*tools.ConcurrentHashMap[MyTag, *MyConn]

	nextport uint8
}

func NewMuxClient(writer MyBusWriter, localAddr Addr) *MyMuxClient {
	mux := &MyMuxClient{
		MyBusWriter: writer,

		localAddr: localAddr,

		ConcurrentHashMap: tools.NewConcurrentHashMap[MyTag, *MyConn](),
	}
	return mux
}

func (m *MyMuxClient) RemoveConn(c *MyConn) {
	m.Remove(c.Tag())
}

func (m *MyMuxClient) Dial(dst Addr) (*MyConn, error) {
	m.Lock()
	defer m.Unlock()

	if m.Size() > 254 {
		return nil, fmt.Errorf("no other ports")
	}
	f := NewCtrlFrame(m.localAddr, dst, m.nextport, Request, 0, 0)
	// 留出 port 0
	for m.Contains(f.Tag()) || m.nextport == 0 {
		m.nextport++
		f.SetPort(m.nextport)
	}
	cBus, _ := NewPipeBusPair()
	c := NewConn(cBus, f.Tag(), m.localAddr, dst, m.nextport)

	// 请求建立链接
	m.SendFrame(f)
	m.PutIfAbsent(c.Tag(), c)

	// // debug
	// log.Println("mapmapmap after dial")
	// m.PrintMap()

	m.nextport++

	return c, nil
}

func (m *MyMuxClient) ReadDaemon(c MyBusReader) {
	c.Lock()
	defer c.Unlock()

	for {
		f, _ := c.RecvFrame()
		// log.Println("!!c", f) // debug
		switch f.Command() {
		case Request:
			// 不会有的，拒绝链接
			m.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0))
			continue
		case Accept:
			continue
		default:
			// 其他情况直接转发
			if conn, exist := m.Get(f.Tag()); exist {
				conn.PutFrame(f)
			} else {
				// // debug
				// log.Println("mapmapmap not exist @ client")
				// m.PrintMap() // debug
				// log.Println(f.Tag())

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

func (m *MyMuxClient) PrintMap() {
	log.Println("print mux map", m.localAddr)
	m.ConcurrentHashMap.ForEach(func(key MyTag, value *MyConn) {
		fmt.Println(key, value)
	})
}
