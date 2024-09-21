package mymux

import (
	"encoding/binary"
	"log"
	"strconv"
)

type Command uint8

func (cmd Command) String() string {
	switch cmd {
	case Data:
		return "Data"
	case Close:
		return "Close"
	case Aloha:
		return "Aloha"
	case Request:
		return "Request"
	case Acknowledge:
		return "Acknowledge"
	default:
		return "Unknown"
	}
}

type Addr uint16

func (a Addr) NetWork() string {
	return "mymux"
}

func (a Addr) String() string {
	return strconv.Itoa(int(a))
}

const (
	FrameHeadLength int = 8

	// for conn
	Data  Command = 0
	Close Command = 1
	Aloha Command = 4
	// for mux
	Request     Command = 1<<6 | 1
	Acknowledge Command = 1<<6 | 2
)

type MyFrame []byte

func NewCtrlFrame(source, destination Addr, port uint8, command Command, sequenceNumber, acknowledgeNumber uint8) MyFrame {
	// 创建一个新的 CtrlFrame，长度为头部长度
	f := make(MyFrame, FrameHeadLength)
	f.SetSource(source)
	f.SetDestination(destination)
	f.SetPort(port)
	f.SetCommand(command)
	f.SetSequenceNumber(sequenceNumber)
	f.SetAcknowledgeNumber(acknowledgeNumber)
	return f
}

func NewDataFrame(source, destination Addr, port uint8, sequenceNumber, acknowledgeNumber uint8, data []byte) MyFrame {
	f := make(MyFrame, FrameHeadLength+len(data))
	f.SetSource(source)
	f.SetDestination(destination)
	f.SetPort(port)
	f.SetSequenceNumber(sequenceNumber)
	f.SetAcknowledgeNumber(acknowledgeNumber)
	f.SetData(data)
	return f
}

func PrintFrame(f MyFrame) {
	log.Printf("%d->%d:%d,%s, %s\n",
		f.Source(), f.Destination(),
		f.Port(), f.Command().String(),
		f.Data())
}

func (f MyFrame) Tag() MyTag {
	var tag MyTag
	copy(tag[:], f[:TagLength])
	return tag
}

// 获取源地址
func (f MyFrame) Source() Addr {
	return Addr(binary.BigEndian.Uint16(f[0:2])) // 使用大端字节序读取
}

// 获取目的地址
func (f MyFrame) Destination() Addr {
	return Addr(binary.BigEndian.Uint16(f[2:4])) // 使用大端字节序读取
}

// 获取端口
func (f MyFrame) Port() uint8 {
	return f[4] // 假设 Port 在第 5 个字节
}

// 获取数据类型
func (f MyFrame) Command() Command {
	return Command(f[5]) // 假设 Command 在第 6 个字节
}

// 获取序列号
func (f MyFrame) SequenceNumber() uint8 {
	return f[6] // 假设 SequenceNumber 在第 7 个字节
}

// 获取序列号
func (f MyFrame) AcknowledgeNumber() uint8 {
	return f[7] // 假设 SequenceNumber 在第 7 个字节
}

// 获取数据内容
func (f MyFrame) Data() []byte {
	return f[FrameHeadLength:] // 假设数据内容从第 8 个字节开始
}

// 设置源地址
func (f MyFrame) SetSource(source Addr) {
	binary.BigEndian.PutUint16(f[0:2], uint16(source)) // 使用大端字节序写入
}

// 设置目的地址
func (f MyFrame) SetDestination(destination Addr) {
	binary.BigEndian.PutUint16(f[2:4], uint16(destination)) // 使用大端字节序写入
}

// 设置端口
func (f MyFrame) SetPort(port uint8) {
	f[4] = port // 假设 Port 在第 5 个字节
}

func (f MyFrame) SetCommand(command Command) {
	f[5] = byte(command)
}

// 设置序列号
func (f MyFrame) SetSequenceNumber(sequence uint8) {
	f[6] = sequence // 假设 SequenceNumber 在第 7 个字节
}

func (f MyFrame) SetAcknowledgeNumber(acknowledge uint8) {
	f[7] = acknowledge // 假设 SequenceNumber 在第 7 个字节
}

// 设置数据内容
func (f MyFrame) SetData(data []byte) int {
	f[5] = byte(Data)
	return copy(f[FrameHeadLength:], data) // 假设数据内容从第 8 个字节开始
}
