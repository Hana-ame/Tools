package mymux

import (
	"encoding/binary"
	"log"
	"strconv"
)

type Command uint8

func (cmd Command) ToString() string {
	switch cmd {
	case Data:
		return "Data"
	case Close:
		return "Close"
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

	// for mux
	Request     Command = 1<<6 | 1
	Acknowledge Command = 1<<6 | 2
)

type MyFrame interface {
	Tag() MyTag

	// 源地址 [0:2]
	Source() Addr
	// 目的地址 [2:4]
	Destination() Addr
	// 端口号只有单向有效，不同服务请用不同的目的地址 [4]
	Port() uint8
	// Data = 0, Ctrl != 0 [5]
	Command() Command
	// 窗口大小 max = 127， [6]
	SequenceNumber() uint8
	AcknowledgeNumber() uint8 // 对不齐不做了

	Data() []byte
}

type CtrlFrame []byte

func NewCtrlFrame(source, destination Addr, port uint8, command Command, sequenceNumber, acknowledgeNumber uint8) CtrlFrame {
	// 创建一个新的 CtrlFrame，长度为头部长度
	f := make(CtrlFrame, FrameHeadLength)
	f.SetSource(source)
	f.SetDestination(destination)
	f.SetPort(port)
	f.SetCommand(command)
	f.SetSequenceNumber(sequenceNumber)
	f.SetAcknowledgeNumber(acknowledgeNumber)
	return f
}

func (f CtrlFrame) Tag() MyTag {
	var tag MyTag
	copy(tag[:], f[:TagLength])
	return tag
}

// 获取源地址
func (f CtrlFrame) Source() Addr {
	return Addr(binary.BigEndian.Uint16(f[0:2])) // 使用大端字节序读取
}

// 获取目的地址
func (f CtrlFrame) Destination() Addr {
	return Addr(binary.BigEndian.Uint16(f[2:4])) // 使用大端字节序读取
}

// 获取端口
func (f CtrlFrame) Port() uint8 {
	return f[4] // 假设 Port 在第 5 个字节
}

// 获取数据类型
func (f CtrlFrame) Command() Command {
	return Command(f[5]) // 假设 Command 在第 6 个字节
}

// 获取序列号
func (f CtrlFrame) SequenceNumber() uint8 {
	return f[6] // 假设 SequenceNumber 在第 6 个字节
}

func (f CtrlFrame) AcknowledgeNumber() uint8 {
	return f[7]
}

// 设置源地址
func (f CtrlFrame) SetSource(source Addr) {
	binary.BigEndian.PutUint16(f[0:2], uint16(source)) // 使用大端字节序写入
}

// 设置目的地址
func (f CtrlFrame) SetDestination(destination Addr) {
	binary.BigEndian.PutUint16(f[2:4], uint16(destination)) // 使用大端字节序写入
}

// 设置端口
func (f CtrlFrame) SetPort(port uint8) {
	f[4] = port // 假设 Port 在第 5 个字节
}

func (f CtrlFrame) SetCommand(command Command) {
	f[5] = byte(command)
}

// 设置序列号
func (f CtrlFrame) SetSequenceNumber(sequence uint8) {
	f[6] = sequence // 假设 SequenceNumber 在第 6 个字节
}

func (f CtrlFrame) SetAcknowledgeNumber(acknowledge uint8) {
	f[7] = acknowledge // 假设 SequenceNumber 在第 7 个字节
}

func (f CtrlFrame) Data() []byte {
	return f[FrameHeadLength:]
}

type DataFrame []byte

func NewDataFrame(source, destination Addr, port uint8, sequenceNumber, acknowledgeNumber uint8, data []byte) DataFrame {
	f := make(DataFrame, FrameHeadLength+len(data))
	f.SetSource(source)
	f.SetDestination(destination)
	f.SetPort(port)
	f.SetSequenceNumber(sequenceNumber)
	f.SetAcknowledgeNumber(acknowledgeNumber)
	f.SetData(data)
	return f
}

func PrintFrame(f DataFrame) {
	log.Printf("%d->%d:%d,%s, %s\n",
		f.Source(), f.Destination(),
		f.Port(), f.Command().ToString(),
		f.Data())
}

func (f DataFrame) Tag() MyTag {
	var tag MyTag
	copy(tag[:], f[:TagLength])
	return tag
}

// 获取源地址
func (f DataFrame) Source() Addr {
	return Addr(binary.BigEndian.Uint16(f[0:2])) // 使用大端字节序读取
}

// 获取目的地址
func (f DataFrame) Destination() Addr {
	return Addr(binary.BigEndian.Uint16(f[2:4])) // 使用大端字节序读取
}

// 获取端口
func (f DataFrame) Port() uint8 {
	return f[4] // 假设 Port 在第 5 个字节
}

// 获取数据类型
func (f DataFrame) Command() Command {
	return Command(f[5]) // 假设 Command 在第 6 个字节
}

// 获取序列号
func (f DataFrame) SequenceNumber() uint8 {
	return f[6] // 假设 SequenceNumber 在第 7 个字节
}

// 获取序列号
func (f DataFrame) AcknowledgeNumber() uint8 {
	return f[7] // 假设 SequenceNumber 在第 7 个字节
}

// 获取数据内容
func (f DataFrame) Data() []byte {
	return f[FrameHeadLength:] // 假设数据内容从第 8 个字节开始
}

// 设置源地址
func (f DataFrame) SetSource(source Addr) {
	binary.BigEndian.PutUint16(f[0:2], uint16(source)) // 使用大端字节序写入
}

// 设置目的地址
func (f DataFrame) SetDestination(destination Addr) {
	binary.BigEndian.PutUint16(f[2:4], uint16(destination)) // 使用大端字节序写入
}

// 设置端口
func (f DataFrame) SetPort(port uint8) {
	f[4] = port // 假设 Port 在第 5 个字节
}

// 设置序列号
func (f DataFrame) SetSequenceNumber(sequence uint8) {
	f[6] = sequence // 假设 SequenceNumber 在第 7 个字节
}

func (f DataFrame) SetAcknowledgeNumber(acknowledge uint8) {
	f[7] = acknowledge // 假设 SequenceNumber 在第 7 个字节
}

// 设置数据内容
func (f DataFrame) SetData(data []byte) int {
	f[5] = byte(Data)
	return copy(f[FrameHeadLength:], data) // 假设数据内容从第 8 个字节开始
}
