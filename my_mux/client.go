package mymux

import (
	"fmt"
	"log"

	tools "github.com/Hana-ame/udptun/Tools"
	"github.com/Hana-ame/udptun/Tools/debug"
)

// portMap 用于管理端口的使用情况，使用位图实现。
type portMap [32]byte

// ContainsPort 检查指定端口是否被占用。
func (m *portMap) ContainsPort(i uint8) bool {
	return 0 != m[i/8]&(1<<(i%8))
}

// SetPort 设置指定端口为占用状态。
func (m *portMap) SetPort(i uint8) {
	m[i/8] |= (1 << (i % 8))
}

// RemovePort 移除指定端口的占用状态。
func (m *portMap) RemovePort(i uint8) {
	m[i/8] &= ^(1 << (i % 8))
}

// NewClientFrameConn 创建一个新的客户端帧连接，发送控制帧并等待接受的响应。
func NewClientFrameConn(bus MyBus, remote, local Addr, port uint8) (*MyFrameConn, error) {
	bus.SendFrame(NewCtrlFrame(local, remote, port, Request, 0, 0)) // 发送请求控制帧
	f, e := bus.RecvFrame()                                         // 接收响应帧
	if e != nil {
		debug.E("NewClientFrameConn", e)
		return nil, e
	}
	if f.Command() != Accept { // 检查是否被接受
		debug.I("NewClientFrameConn", "f not accepted")
		return nil, fmt.Errorf("not accepted")
	}

	return NewFrameConn(bus, local, remote, port), nil // 返回新创建的帧连接
}

// MyClient 定义客户端结构，包含本地地址和端口映射。
type MyClient struct {
	MyBus

	localAddr Addr

	*tools.ConcurrentHashMap[MyTag, MyBus] // 存储标签和总线的映射

	*portMap       // 端口映射
	nextport uint8 // 下一个可用端口
}

// NewClient 创建一个新的客户端实例。
func NewClient(bus MyBus, localAddr Addr) *MyClient {
	client := &MyClient{
		MyBus: bus,

		localAddr: localAddr,

		ConcurrentHashMap: tools.NewConcurrentHashMap[MyTag, MyBus](),
		portMap:           &portMap{},
	}
	return client
}

// ReadDaemon 读取守护进程，处理接收到的帧。
func (c *MyClient) ReadDaemon() error {
	c.Lock()
	defer c.Unlock()

	for {
		f, err := c.RecvFrame() // 接收帧
		if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
			c.Close()
			return err
		}
		switch f.Command() {
		case Request: // 请求命令
			c.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0)) // 拒绝请求
		// case Accept: // 要接收的情况（未使用）
		// 	continue
		default:
			// 其他情况直接转发
			if b, exist := c.Get(f.Tag()); exist {
				b.SendFrame(f) // 转发帧
			} else {
				log.Println(f.Tag(), b, exist)
				if f.Command() == Close { // 如果是关闭命令，跳过
					continue
				}
				c.SendFrame(NewCtrlFrame(f.Destination(), f.Source(), f.Port(), Close, 0, 0)) // 拒绝
			}
		}
	}
}

// Dial 拨号到指定地址，创建连接并返回帧连接。
func (s *MyClient) Dial(dst Addr) (*MyFrameConn, error) {
	// 查找下一个可用端口
	for s.ContainsPort(s.nextport) {
		s.nextport++
	}
	cBus, sBus := NewPipeBusPair() // 创建管道总线对
	go func(b MyBus, tag MyTag, port uint8) {
		// bus对面是client conn
		for {
			f, err := b.RecvFrame() // 接收帧
			if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
				s.Remove(tag)      // 移除标签
				s.RemovePort(port) // 移除端口
			}
			err = s.SendFrame(f) // 转发帧
			if err != nil && (err.Error() == ERR_BUS_CLOSED || err.Error() == ERR_PIPE_CLOSED) {
				s.Remove(tag)      // 移除标签
				s.RemovePort(port) // 移除端口
			}
		}
	}(sBus, NewTag(dst, s.localAddr, s.nextport), s.nextport)

	s.PutIfAbsent(NewTag(s.localAddr, dst, s.nextport), sBus) // 存储标签和总线

	c, e := NewClientFrameConn(cBus, s.localAddr, dst, s.nextport) // 创建帧连接

	s.nextport++ // 更新下一个端口

	return c, e // 返回帧连接和错误
}
