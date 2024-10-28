package mymux

import (
	"encoding/binary"
	"net"
	"sync"
)

type TCPNOde struct {
	net.Conn
	Node
}

func TCP(conn net.Conn, node Node) error {
	var err error
	cond := sync.NewCond(&sync.Mutex{})

	go func() {
		err = TCPReadCopy(conn, node)
		cond.Signal() // 通知主协程
	}()
	go func() {
		err = TCPWriteCopy(conn, node)
		cond.Signal() // 通知主协程
	}()

	// 等待条件变量信号
	cond.Wait()
	conn.Close()

	return err
}

func TCPReadCopy(conn net.Conn, node Node) (err error) {
	for {
		size := make([]byte, 2)
		_, err = conn.Read(size)
		if err != nil {
			return
		}

		buffer := make([]byte, int(binary.BigEndian.Uint16(size)))

		_, err = conn.Read(size)
		if err != nil {
			return
		}

		err = node.SendFrame(buffer)
		if err != nil {
			return
		}
	}
}

func TCPWriteCopy(conn net.Conn, node Node) error {
	size := make([]byte, 2)
	for {
		f, err := node.RecvFrame()
		if err != nil {
			return err
		}
		binary.BigEndian.PutUint16(size, uint16(len(f)))

		_, err = conn.Write(size)
		if err != nil {
			return err
		}
		_, err = conn.Write(f)
		if err != nil {
			return err
		}
	}
}
