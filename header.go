package tools

import "net/http"

type Header struct {
	http.Header
}

func (h Header) Add(key, value string) {
	if value == "" {
		return
	}
	h.Header.Add(key, value)
}

func NewHeader(header http.Header) Header {
	if header == nil {
		header = http.Header{}
	}
	return Header{Header: header}
}
