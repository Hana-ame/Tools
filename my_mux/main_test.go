package mymux

import (
	"fmt"
	"io"
	"log"
	"testing"
	"time"
)

func TestXxx(t *testing.T) {
	a2bReader, b2bWriter := io.Pipe()
	b2bReader, b2aWriter := io.Pipe()
	b2aReader, a2aWriter := io.Pipe()
	a2aReader, a2bWriter := io.Pipe()

	go func() {
		buf := make([]byte, 1500)
		for {
			n, _ := b2bReader.Read(buf)
			log.Println("pipe b:", buf[:n])
			b2bWriter.Write(buf[:n])
		}
	}()
	go func() {
		buf := make([]byte, 1500)
		for {
			n, _ := a2aReader.Read(buf)
			log.Println("pipe a:", buf[:n])
			a2aWriter.Write(buf[:n])
		}
	}()

	aBus := NewReaderWriterBus(a2bReader, a2bWriter)
	bBus := NewReaderWriterBus(b2aReader, b2aWriter)

	aMux := NewMuxServer(aBus)
	go aMux.ReadDaemon(aBus)

	bMux := NewMuxClient(bBus)
	go bMux.ReadDaemon(bBus)

	go handleServer(aMux)
	go handleClient(bMux)
	go handleClient(bMux)

	time.Sleep(30 * time.Second)
}

func handleServer(server *MyMuxServer) {
	log.Println("handleServer")
	for {
		c := server.Accept()
		go handleServerConn(c)
	}
}

func handleServerConn(c *MyConn) {
	log.Println("handleConn")
	go func() {
		buf := make([]byte, 1500)
		for {
			n, err := c.Read(buf)
			if err != nil {
				log.Fatal(err)
			}

			log.Println(c.Tag(), "server recv:", string(buf[:n]))

			c.Write(buf[:n])
		}
	}()

	for i := 0; i < 5; i++ {
		c.Write([]byte(fmt.Sprintf("来自server %d", i)))
		time.Sleep(time.Second)
	}
	time.Sleep(time.Minute)
}

func handleClient(client *MyMuxClient) {
	log.Println("handleClient")
	c, err := client.Dial(5)
	if err != nil {
		log.Fatal(err)
	}
	go func() {
		buf := make([]byte, 1500)
		for {
			n, err := c.Read(buf)
			if err != nil {
				log.Fatal(err)
			}
			log.Println(c.Tag(), "client recv:", string(buf[:n]))
		}
	}()

	for i := 0; i < 5; i++ {
		c.Write([]byte(fmt.Sprintf("来自client %d", i)))
		time.Sleep(time.Second)
	}
	time.Sleep(time.Minute)
}
