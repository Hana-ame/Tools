package handlerFunc

import (
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

// func main() {
// 	router := gin.Default()

// 	router.GET("/timestamp", GetTimestamp)
// 	router.GET("/timestamp/s", GetTimestampSeconds)
// 	router.GET("/timestamp/ms", GetTimestampMilliseconds)
// 	router.GET("/timestamp/us", GetTimestampMicroseconds)
// 	router.GET("/timestamp/ns", GetTimestampNanoseconds)

// 	router.Run()
// }

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
