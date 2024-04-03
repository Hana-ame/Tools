// @ 2023-12-21
// azure-go @ 2023-12-21

package myfetch

import (
	"io"
	"net/http"
)

var defaultHeader = make(http.Header)

func SetDefaultHeader(header http.Header) {
	defaultHeader = header
}

func Do(req *http.Request) (*http.Response, error) {
	for k, vs := range defaultHeader {
		if req.Header.Get(k) == "" {
			for _, v := range vs {
				req.Header.Add(k, v)
			}
		}
	}
	return Client().Do(req)
}

func NewRequest(method, url string, header http.Header, body io.Reader) (*http.Request, error) {

	req, err := http.NewRequest(
		method,
		url,
		body,
	)
	if err != nil {
		return nil, err
	}

	if header != nil {
		req.Header = header
	}

	return req, nil
}

// this function make a request and return a response
func Fetch(method, url string, header http.Header, body io.Reader) (*http.Response, error) {

	req, err := NewRequest(method, url, header, body)
	if err != nil {
		return nil, err
	}

	return Do(req)
}
