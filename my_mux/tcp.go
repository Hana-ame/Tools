package mymux

import (
	"encoding/binary"
	"net"
)

type TCPNode struct {
	reading bool
	writing bool
	Conn    net.Conn
	Node    // 假设 Node 是一个定义好的接口或结构体
}

func (n *TCPNode) SetConn(c net.Conn) {
	n.Conn = c
}

func (n *TCPNode) SetReading(f bool) {
	n.reading = f
}

func (n *TCPNode) SetWriting(f bool) {
	n.writing = f
}

func (n *TCPNode) ReadCopy() error {
	defer n.SetReading(false)
	n.reading = true
	for n.reading {
		size := make([]byte, 2)
		_, err := n.Conn.Read(size)
		if err != nil {
			return err
		}

		buffer := make([]byte, binary.BigEndian.Uint16(size))
		_, err = n.Conn.Read(buffer)
		if err != nil {
			return err
		}

		err = n.SendFrame(buffer)
		if err != nil {
			return err
		}
	}
	return nil
}

func (n *TCPNode) WriteCopy() error {
	defer n.SetWriting(false)
	n.writing = true
	for n.writing {
		f, err := n.RecvFrame()
		if err != nil {
			return err
		}

		size := make([]byte, 2)
		binary.BigEndian.PutUint16(size, uint16(len(f)))

		_, err = n.Conn.Write(size)
		if err != nil {
			return err
		}
		_, err = n.Conn.Write(f)
		if err != nil {
			return err
		}
	}
	return nil
}
