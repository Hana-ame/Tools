package mymux

import (
	"sync"

	log "github.com/Hana-ame/udptun/Tools/debug"
)

type Error string

func (e Error) Error() string {
	return string(e)
}

const (
	ERR_PIPE_CLOSED Error = "my pipe closed" // 管道关闭错误信息
)

// MyPipe 定义了一个管道结构，用于在读取和写入之间传递数据。
type MyPipe struct {
	*sync.Cond // 条件变量，用于同步
	sync.Mutex // 互斥锁，确保只有一个读取协程在运行

	f      MyFrame // 存储要传递的帧
	closed bool    // 管道是否关闭
}

// SendFrame 发送帧到管道。
func (p *MyPipe) SendFrame(f MyFrame) (err error) {
	p.L.Lock() // 锁定互斥锁
	// 当帧不为空且管道未关闭时，等待
	for !(p.f == nil || p.closed) {
		p.Wait()
	}
	if p.closed {
		err = ERR_PIPE_CLOSED
	}
	p.f = f // 设置帧
	p.L.Unlock()

	p.Broadcast() // 唤醒等待的协程
	return
}

// RecvFrame 从管道接收帧。
func (p *MyPipe) RecvFrame() (f MyFrame, err error) {
	p.L.Lock() // 锁定互斥锁
	// 当帧为空且管道未关闭时，等待
	for !(p.f != nil || p.closed) {
		p.Wait()
	}

	if p.closed {
		err = ERR_PIPE_CLOSED
	}
	f = p.f   // 获取帧
	p.f = nil // 清空帧
	p.L.Unlock()

	p.Broadcast() // 唤醒等待的协程
	return f, err
}

// Close 关闭管道并广播唤醒所有等待的协程。
func (p *MyPipe) Close() error {
	p.L.Lock() // 锁定互斥锁
	// 要sending最后一个package，这是为了正常关闭。
	for !(p.f == nil || p.closed) {
		p.Wait()
	}
	p.closed = true
	p.L.Unlock()
	p.Broadcast() // 广播信号
	return nil
}

// NewPipe 创建一个新的管道，返回读取和写入接口。
func NewPipe() (MyBus, MyBus) {
	pipe := &MyPipe{Cond: sync.NewCond(&sync.Mutex{})}
	return pipe, pipe // 返回同一个管道的读写接口
}

// NewDebugPipe 创建一个带调试功能的管道。
func NewDebugPipe(tag string) (MyBusReader, MyBusWriter) {
	pipeR := &MyPipe{Cond: sync.NewCond(&sync.Mutex{})}
	pipeW := &MyPipe{Cond: sync.NewCond(&sync.Mutex{})}
	go func() {
		for {
			f, e := pipeW.RecvFrame() // 从写管道接收帧
			if e != nil {
				log.E(tag, e) // 记录错误
			} else if len(f) < FrameHeadLength {
				log.W(tag, "length = ", len(f)) // 记录警告
			} else {
				log.D(tag, SprintFrame(f)) // 打印帧内容
				e = pipeR.SendFrame(f)     // 发送帧到读管道
				if e != nil {
					log.E(tag, e) // 记录错误
				}
			}
		}
	}()
	return pipeR, pipeW // 返回读写管道
}
