package mymux

import (
	"log"
	"sync"
	"testing"
	"time"
)

func handleClientConn(c *MyFrameConn) {
	for {
		f, e := c.ReadFrame()
		if e != nil {
			log.Println(e)
			if e.Error() == ERR_BUS_CLOSED || e.Error() == ERR_PIPE_CLOSED {
				return
			}
			continue
		}
		log.Println("client recv:", string(f))
	}
}

func handleAcceptedConn(c *MyFrameConn) {
	for {
		f, e := c.ReadFrame()
		if e != nil {
			log.Println(e)
			if e.Error() == ERR_BUS_CLOSED || e.Error() == ERR_PIPE_CLOSED {
				return
			}
			continue
		}
		log.Println("serve recv:", string(f))
	}
}

func TestClient(t *testing.T) {
	cb, sb := NewPipeBusPair()
	server := NewServer(sb, 0)
	go server.ReadDeamon()
	go func() {
		for {
			c := server.Accpet()
			go handleAcceptedConn(c)

			time.Sleep(time.Second)
			c.WriteFrame([]byte("from server 1"))
			time.Sleep(time.Second)
			c.WriteFrame([]byte("from server 2"))
		}
	}()

	client := NewClient(cb, 1)
	go client.ReadDaemon()
	{
		c, e := client.Dial(0)
		if e != nil {
			t.Error(e)
		}
		go handleClientConn(c)
		// time.Sleep(time.Second)
		_, e = c.WriteFrame([]byte("from client 11"))
		if e != nil {
			t.Error(e)

		}
		_, e = c.WriteFrame([]byte("from client 12"))
		if e != nil {
			t.Error(e)

		}
	}
	{
		c, e := client.Dial(0)
		if e != nil {
			t.Error(e)
		}
		go handleClientConn(c)
		time.Sleep(time.Second)
		c.WriteFrame([]byte("from client 21"))
		c.WriteFrame([]byte("from client 22"))
	}
	time.Sleep(time.Second * 20)
}

// func TestClient(t *testing.T) {
// 	cb, sb := NewBusPipe()
// 	server := NewServer(sb, 0)
// 	go server.ReadDeamon()
// 	go func() {
// 		for {
// 			c := server.Accpet()
// 			go handleAcceptedConn(c)

// 			time.Sleep(time.Second)
// 			c.WriteFrame([]byte("from server 1"))
// 			time.Sleep(time.Second)
// 			c.WriteFrame([]byte("from server 2"))
// 		}
// 	}()
// 	{
// 		client := NewClient(cb, 1, 2, 3)
// 		go handleClientConn(client)
// 		client.WriteFrame([]byte("from client 11"))
// 		client.WriteFrame([]byte("from client 12"))
// 	}
// 	{
// 		client := NewClient(cb, 1, 2, 4)
// 		go handleClientConn(client)
// 		client.WriteFrame([]byte("from client 21"))
// 		client.WriteFrame([]byte("from client 22"))
// 		client.Close()
// 		client.WriteFrame([]byte("from client 25"))

// 	}
// 	time.Sleep(time.Minute)

// }

func TestCond(t *testing.T) {
	var b bool
	var c sync.Cond = *sync.NewCond(&sync.Mutex{})
	go func() {
		c.L.Lock()
		for !b {
			c.Wait()
			log.Println("waiting 1")
		}
		c.L.Unlock()

		time.Sleep(time.Second)
		c.Signal()
		time.Sleep(time.Second)
		b = false
	}()
	go func() {
		c.L.Lock()
		for !b {
			c.Wait()
			log.Println("waiting 0")
		}
		c.L.Unlock()

		time.Sleep(time.Second)
		b = false
		time.Sleep(time.Second)
		c.Signal()

	}()
	time.Sleep(time.Second * 2)
	b = true
	c.Broadcast()
	c.L.Lock()
	for b {
		c.Wait()
		log.Println("waiting 2")
	}
	c.L.Unlock()
	log.Println("OK")
}
