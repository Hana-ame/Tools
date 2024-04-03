// azure-go @ 2023-12-21
// eh-web-viewer

package myfetch

import "net/http"

type clients struct {
	cnt     uint8
	clients []*http.Client
}

func NewClients() *clients {
	return new(clients)
}

func (cs *clients) Client() *http.Client {
	cs.cnt++
	if len(cs.clients) == 0 {
		return http.DefaultClient
	} else {
		return cs.clients[int(cs.cnt)%len(cs.clients)]
	}
}

func (cs *clients) SetClients(clients []*http.Client) {
	cs.clients = clients
}

// public methods

var DefaultClients *clients = &clients{cnt: 0, clients: []*http.Client{}}

func Client() *http.Client {
	return DefaultClients.Client()
}

func SetClients(clients []*http.Client) {
	DefaultClients.SetClients(clients)
}
