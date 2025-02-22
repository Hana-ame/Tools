package tools

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// 防止添加""作为header的外包装
type Header struct {
	http.Header
}

func (h Header) Add(key, value string) {
	if value == "" {
		return
	}
	h.Header.Add(key, value)
}

func (h Header) GetAllKeys() []string {
	s := make([]string, 0, len(h.Header))
	for k := range h.Header {
		s = append(s, k)
	}
	return s
}

// 仅为了防止“”作为header被添加
func NewHeader(header http.Header) Header {
	if header == nil {
		header = http.Header{}
	}
	return Header{Header: header}
}

func CopyHeader(c *gin.Context, header http.Header) {
	for k, vs := range header {
		if c.Writer.Header().Get(k) != "" {
			continue
		}
		for _, v := range vs {
			c.Writer.Header().Add(k, v)
		}
	}
}
