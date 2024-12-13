package handler

import (
	"net/http"
	"strconv"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

var mu sync.Mutex
var lastTime int64
var lastSequence int64

func NewTimeStamp() int64 {
	mu.Lock()
	defer mu.Unlock()
	now := time.Now().UnixMilli() << 16

	if now == lastTime {
		lastSequence += 1
	} else {
		// fmt.Println(lastSequence)
		lastTime = now
		lastSequence = 0
	}
	return now + lastSequence
}

func GetTimestamp(c *gin.Context) {
	ts := float64(time.Now().UnixNano()) * (float64(65536) / float64(1_000_000))
	c.String(http.StatusOK, strconv.Itoa(int(ts)))
}

func GetTimestampSeconds(c *gin.Context) {
	ts := (time.Now().Unix())
	c.String(http.StatusOK, strconv.Itoa(int(ts)))
}

func GetTimestampMilliseconds(c *gin.Context) {
	ts := (time.Now().UnixNano()) / 1e6
	c.String(http.StatusOK, strconv.Itoa(int(ts)))
}

func GetTimestampMicroseconds(c *gin.Context) {
	ts := (time.Now().UnixNano()) / 1e3
	c.String(http.StatusOK, strconv.Itoa(int(ts)))
}

func GetTimestampNanoseconds(c *gin.Context) {
	ts := (time.Now().UnixNano())
	c.String(http.StatusOK, strconv.Itoa(int(ts)))
}
