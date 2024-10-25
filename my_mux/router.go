package mymux

import (
	tools "github.com/Hana-ame/udptun/Tools"
)

// TODO
type MyRoute struct {
	*tools.ConcurrentHashMap[uint16, *MyBus]
}

func NewRouter() *MyRoute {
	router := &MyRoute{
		ConcurrentHashMap: tools.NewConcurrentHashMap[uint16, *MyBus](),
		// buses: make([]*MyBus, 25),
	}
	return router
}

// func (r *MyRoute) ReadDaemon(b *MyBus) {
// 	for {
// 		f, err := b.RecvFrame()
// 		if err != nil {
// 			log.Println(err)
// 		}
// 		// 怎么处理草泥马
// 	}
// }
