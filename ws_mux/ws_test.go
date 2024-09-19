package wsmux

import (
	"log"
	"net/url"
	"testing"
	"time"

	"github.com/gorilla/websocket"
)

func TestClient(t *testing.T) {
	// WebSocket 服务器的 URL
	u := url.URL{Scheme: "ws", Host: "127.0.0.1:8080", Path: "/ws"}
	log.Println(u)

	// 建立 WebSocket 连接
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()
	log.Println("dial")

	// 发送消息
	msg := "Hello, server!"
	err = c.WriteMessage(websocket.BinaryMessage, []byte(msg))
	if err != nil {
		log.Println("write:", err)
	}
	log.Println("write")

	// 接收消息
	// for {
	_, message, err := c.ReadMessage()
	if err != nil {
		log.Println("read:", err)
		// break
	}
	log.Printf("recv: %s\n", message)
	time.Sleep(1 * time.Second)
	// }

}

func TestMux(t *testing.T) {
	// WebSocket 服务器的 URL
	u := url.URL{Scheme: "ws", Host: "127.0.0.1:8080", Path: "/ws"}
	log.Println(u)

	// 建立 WebSocket 连接
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()
	log.Println("dial")

	mux := NewWsMux(c, MuxSeqClient)

	go func() {
		c := mux.Accept()
		pkg := c.ReadPackage()
		log.Println(pkg)
	}()

	// 发送消息
	subConn, _ := mux.Dial()
	subConn.Write([]byte("你是不是傻逼"))
	// 接收消息
	pkg := subConn.ReadPackage()
	log.Printf("recv: %s\n", pkg.Message)
	time.Sleep(1 * time.Second)
	// }

}

func TestMuxMul(t *testing.T) {
	// WebSocket 服务器的 URL
	u := url.URL{Scheme: "ws", Host: "127.0.0.1:8080", Path: "/ws"}
	log.Println(u)

	// 建立 WebSocket 连接
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()
	log.Println("dial")

	mux := NewWsMux(c, MuxSeqClient)

	go func() {
		c := mux.Accept()
		pkg := c.ReadPackage()
		log.Println(pkg)
	}()

	go dialSendRecv(mux, []byte("卧槽你有病"), 5)
	go dialSendRecv(mux, []byte("卧槽你有病吧"), 5)
	go dialSendRecv(mux, []byte("卧槽你有大病吧"), 5)

	time.Sleep(time.Second * 20)
}

func dialSendRecv(mux *WsMux, msg []byte, times int) {
	c, _ := mux.Dial()
	go func() {
		pkg := c.ReadPackage()
		log.Println(pkg)
	}()
	for i := 0; i < times; i++ {
		c.Write(msg)
	}
}
