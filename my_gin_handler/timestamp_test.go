package handler

import (
	"testing"

	"github.com/gin-gonic/gin"
)

func TestTimestamp(t *testing.T) {

	// func main() {
	router := gin.Default()

	router.GET("/timestamp", GetTimestamp)
	router.GET("/timestamp/s", GetTimestampSeconds)
	router.GET("/timestamp/ms", GetTimestampMilliseconds)
	router.GET("/timestamp/us", GetTimestampMicroseconds)
	router.GET("/timestamp/ns", GetTimestampNanoseconds)

	router.Run()
	// }

}
