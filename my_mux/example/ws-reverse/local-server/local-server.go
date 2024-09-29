package localserver

// import (
// 	"flag"
// 	"net"

// 	"github.com/gorilla/websocket"
// 	"github.com/Hana-ame/udptun/Tools/debug"
// 	mymux "github.com/Hana-ame/udptun/Tools/my_mux"
// )

// func main() {
// 	// 定义命令行参数
// 	wsUrl := flag.String("u", "ws://file.moonchan.xyz/ws/server", "")
// 	dstUrl := flag.Int("l", "localhost:8080", "")

// 	// 解析命令行参数
// 	flag.Parse()

// 	for {
// 		ws, _, e := websocket.DefaultDialer.Dial(*wsUrl, nil)
// 		if e != nil {
// 			debug.E(e)
// 			continue
// 		}

// 		b := &mymux.MyWsBus{Conn: ws}

// 		s := mymux.NewServer(b, 0)
// 		for {
// 			c := s.Accpet()

// 		}

// 	}

// }

// func handleNewConn(ac mymux.MyConn, dstUrl string) {
// 	dc, e := net.Dial("tcp", dstUrl)
// 	if e != nil {
// 		debug.E(e)
// 		return
// 	}

// }
