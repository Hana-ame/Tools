package handler

import (
	"testing"

	"github.com/Hana-ame/neo-moonchan/Tools/debug"
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

func TestNewTimeStamp(t *testing.T) {
	var la int64
	for i := 0; i < 200000; i++ {
		a := NewTimeStamp()
		// fmt.Println(a)
		if la == a {
			debug.F("equal")
		}
		la = a
	}
}
