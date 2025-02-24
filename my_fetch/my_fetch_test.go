// gin-pack @ 2024-04-06

package myfetch

import (
	"fmt"
	"io"
	"log"
	"os"
	"testing"
)

func TestFetch(t *testing.T) {
	fmt.Println("1")
	log.Println(os.Getenv("HTTPS_PROXY")) // it works
	resp, _ := Fetch("GET", "https://chat.moonchan.xyz/api/ping", nil, nil)
	log.Println(resp.Header)
	log.Println(resp.Header.Get("Content-Type"))
	defer resp.Body.Close()
	s, _ := io.ReadAll(resp.Body)
	log.Println(string(s))
}
