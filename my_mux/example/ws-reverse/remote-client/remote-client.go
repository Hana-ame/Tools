package remoteclient

import (
	"io"
	"net"
	"net/http"

	"github.com/Hana-ame/udptun/Tools/debug"
	mymux "github.com/Hana-ame/udptun/Tools/my_mux"
	wsreverse "github.com/Hana-ame/udptun/Tools/my_mux/example/ws-reverse"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
)

// // 定义一个客户端结构体
// type Client struct {
// 	conn *websocket.Conn
// }

// // 定义一个客户端集合
// var clients = make(map[*Client]bool)
// var broadcast = make(chan string)

var Conn = wsreverse.NewConn(
	nil,
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

// 处理WebSocket连接
func HandleWebSocket(c *gin.Context) {
	const Tag = "HandleWebSocket"
	// 升级HTTP连接为WebSocket连接
	ws, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		debug.E(Tag, err.Error())
	}
	// defer ws.Close()

	Conn.SetConn(ws)
	debug.I(Tag, "accept a new conn and set")
}

func init() {
	const Tag = "remote-client"
	bus := wsreverse.NewWsServer(Conn)
	client := mymux.NewClient(bus, 5)

	listener, err := net.Listen("tcp", "127.24.10.4:8080")
	debug.E(Tag, err.Error())

	for {
		conn, err := listener.Accept()
		if err != nil {
			debug.E(Tag, err.Error())
			continue
		}

		muxc, err := client.Dial(5)
		if err != nil {
			conn.Close()
			debug.E(Tag, err.Error())
			continue
		}

		go forward(conn, muxc)

	}
}

func forward(c net.Conn, muxc *mymux.MyFrameConn) {
	muxs := &mymux.MyFrameConnStreamr{MyFrameConn: muxc}
	io.Copy(muxs, c)	
	io.Copy(c, muxs)	
	
}
