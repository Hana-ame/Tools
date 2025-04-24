// SB gpt, not work

package main

import (
	"errors"
	"flag"
	"fmt"
	"io"
	"net"
	"os"
	"syscall"
)

const (
	socks5Version = 0x05
	ipv6OnlyFlag  = true // 强制使用 IPv6
)

var ipstr string

func main() {
	flag.StringVar(&ipstr, "ip", "::1", "ipv6")
	flag.Parse()

	server, err := net.Listen("tcp", "127.0.0.1:1080")
	if err != nil {
		fmt.Printf("Listen error: %v\n", err)
		os.Exit(1)
	}
	defer server.Close()

	fmt.Println("SOCKS5 proxy (IPv6 only) started on :1080,", ipstr)

	for {
		client, err := server.Accept()
		if err != nil {
			fmt.Printf("Accept error: %v\n", err)
			continue
		}
		go handleClient(client)
	}
}

func handleClient(client net.Conn) {
	defer client.Close()

	// 创建强制 IPv6 的 Dialer
	dialer := &net.Dialer{
		LocalAddr: &net.TCPAddr{
			IP: net.ParseIP(ipstr), // 使用本地 IPv6 地址 (::1) 或替换为你需要的特定 IPv6 地址
		},
		Control: func(network, address string, c syscall.RawConn) error {
			if network != "tcp6" {
				return errors.New("ipv4 connections disabled")
			}
			return nil
		},
	}

	// 认证阶段（同标准 SOCKS5 实现）
	if err := auth(client); err != nil {
		fmt.Printf("Auth failed: %v\n", err)
		return
	}

	// 建立连接
	target, err := connect(client, dialer)
	if err != nil {
		fmt.Printf("Connect error: %v\n", err)
		return
	}
	defer target.Close()

	// 数据中继
	go io.Copy(target, client)
	io.Copy(client, target)
}

func auth(client net.Conn) error {
	buf := make([]byte, 256)

	// 读取协议版本和支持的认证方法
	if _, err := io.ReadFull(client, buf[:2]); err != nil {
		return errors.New("read auth header failed")
	}

	// 响应无需认证
	_, err := client.Write([]byte{socks5Version, 0x00})
	return err
}

func connect(client net.Conn, dialer *net.Dialer) (net.Conn, error) {
	buf := make([]byte, 256)

	// 读取请求头
	n, err := io.ReadFull(client, buf[:4])
	if n != 4 || err != nil {
		return nil, errors.New("invalid request header")
	}

	ver, cmd, atyp := buf[0], buf[1], buf[3]
	fmt.Printf("Command: %d, Address Type: %d\n", cmd, atyp)
	if ver != socks5Version || cmd != 0x01 {
		return nil, errors.New("unsupported command")
	}

	// 解析目标地址（支持 IPv6）
	var host string
	switch atyp {
	case 0x01: // IPv4
		return nil, errors.New("ipv4 connections disabled")
	case 0x03: // 域名
		if _, err := io.ReadFull(client, buf[:1]); err != nil {
			return nil, errors.New("invalid domain length")
		}
		domainLen := int(buf[0])
		if _, err := io.ReadFull(client, buf[:domainLen]); err != nil {
			return nil, errors.New("invalid domain")
		}
		host = string(buf[:domainLen])
	case 0x04: // IPv6
		ipv6 := make([]byte, 16)
		if _, err := io.ReadFull(client, ipv6); err != nil {
			return nil, errors.New("invalid IPv6 address")
		}
		host = net.IP(ipv6).String()
	default:
		return nil, errors.New("unsupported address type")
	}

	// 读取端口
	if _, err := io.ReadFull(client, buf[:2]); err != nil {
		return nil, errors.New("invalid port")
	}
	port := fmt.Sprintf("%d", int(buf[0])<<8|int(buf[1]))

	// 强制使用 IPv6 连接
	target, err := dialer.Dial("tcp6", net.JoinHostPort(host, port))
	if err != nil {
		return nil, fmt.Errorf("dial failed: %v", err)
	}

	// 构造 IPv6 响应包
	resp := []byte{
		socks5Version, 0x00, 0x00, 0x04,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		buf[0], buf[1],
	}
	_, err = client.Write(resp)
	if err != nil {
		fmt.Println(err.Error())
	}
	return target, err
}
