package wsmux

import (
	"sync"

	"github.com/gorilla/websocket"
)

const (
	MuxSeqServer uint16 = 0
	MuxSeqClient uint16 = 1
)

type WsMux struct {
	sync.RWMutex

	*websocket.Conn

	SeqN uint16

	acceptingConnChan     chan *WsConn
	acceptingConnChanSize int
	Conns                 map[uint16]*WsConn

	err error
}

func NewWsMux(conn *websocket.Conn, seqType uint16) *WsMux {
	acceptingConnChanSize := 5
	wsMux := &WsMux{
		Conn:                  conn,
		SeqN:                  seqType,
		acceptingConnChanSize: acceptingConnChanSize,
		acceptingConnChan:     make(chan *WsConn, acceptingConnChanSize),
		Conns:                 make(map[uint16]*WsConn),
	}
	go wsMux.readDaemon(conn)
	return wsMux
}

func (w *WsMux) setErrorIfPresent(err error) bool {
	if err != nil {
		w.err = err
		return true
	}
	return false
}

func (w *WsMux) generateSequenceNumber() uint16 {
	w.SeqN += 2
	return w.SeqN
}

func (w *WsMux) readDaemon(conn *websocket.Conn) {
	for {
		_, data, err := conn.ReadMessage()
		if w.setErrorIfPresent(err) {
			return // Exit on error
		}

		pkg, err := FromBytes(data)
		if w.setErrorIfPresent(err) {
			continue
		}

		if w.GetConn(pkg.ID) == nil {
			for len(w.acceptingConnChan) > 0 {
				(<-w.acceptingConnChan).Close()
			}
			newConn := NewWsConn(pkg.ID, w)
			w.AddConn(newConn)
			w.acceptingConnChan <- newConn
		}
		w.GetConn(pkg.ID).PutPackage(pkg)
	}
}
func (w *WsMux) AddConn(conn *WsConn) *WsConn {
	w.Lock()
	defer w.Unlock()
	w.Conns[conn.ID] = conn
	return conn
}

func (w *WsMux) GetConn(id uint16) *WsConn {
	w.RLock()
	defer w.RUnlock()
	return w.Conns[id]
}

func (w *WsMux) DeleteConn(id uint16) {
	w.Lock()
	defer w.Unlock()
	delete(w.Conns, id)
}

func (w *WsMux) Accept() *WsConn {
	return <-w.acceptingConnChan
}

// always no error
func (w *WsMux) Dial() (*WsConn, error) {
	conn := NewWsConn(w.generateSequenceNumber(), w)
	w.AddConn(conn)
	return conn, nil
}

// concurrent write to websocket connection
func (w *WsMux) WriteMessage(messageType int, message []byte) error {
	w.Lock()
	defer w.Unlock()
	return w.Conn.WriteMessage(messageType, message)
}
