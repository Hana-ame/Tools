package tools

import "net/http"

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

func NewHeader(header http.Header) Header {
	if header == nil {
		header = http.Header{}
	}
	return Header{Header: header}
}
