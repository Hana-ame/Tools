package handler

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"sort"

	"go-tools/Tools/orderedmap"
	"github.com/gin-gonic/gin"
)

func EchoJSON(c *gin.Context) {

	o := orderedmap.New()
	for k, v := range c.Request.Header {
		o.Set(k, v)
	}
	o.SortKeys(sort.Strings)

	c.JSONP(http.StatusOK, o)

}

func Echo(c *gin.Context) {

	println := func(format string, a ...any) {
		str := fmt.Sprintf(format, a...)
		c.String(200, (str)+"\n")
	}

	println(`----------head----------`)
	println(c.Request.Method)
	println(c.Request.Host)
	println("%v", c.Request.URL)
	println(c.Request.Proto)

	o := orderedmap.New()
	for k, v := range c.Request.Header {
		o.Set(k, v)
	}
	o.SortKeys(sort.Strings)

	for _, k := range o.Keys() {
		for _, v := range o.GetOrDefault(k, []string{"!error!"}).([]string) {
			println("%v: %v", k, v)
		}
	}
	println(`----------body----------`)

	body, err := io.ReadAll(c.Request.Body)
	if err != nil {
		log.Fatal(err)
		println("%v", err)
	} else {
		println(string(body))
	}
	println(`----------end of body----------`)

}
