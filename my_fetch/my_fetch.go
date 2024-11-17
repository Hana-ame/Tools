// gin-pack @ 2024-04-06
// @ 2023-12-21
// azure-go @ 2023-12-21

package myfetch

import (
	"io"
	"net/http"
)

type fetcher struct {
	header     http.Header
	clientPool *clientPool
}

func (f *fetcher) SetDefaultHeader(header http.Header) {
	f.header = header
}

func (f *fetcher) SetClientPool(clientPool *clientPool) {
	f.clientPool = clientPool
}

func (f *fetcher) Do(req *http.Request) (*http.Response, error) {
	clientPool := f.clientPool
	defaultHeader := f.header

	// 如果没有被指定过，那么defaultHeader中有的东西就放进去
	for k, vs := range defaultHeader {
		if req.Header.Get(k) == "" {
			for _, v := range vs {
				req.Header.Add(k, v)
			}
		}
	}
	return clientPool.Client().Do(req)
}

// this function make a request and return a response
func (f *fetcher) Fetch(method, url string, header http.Header, body io.Reader) (*http.Response, error) {

	req, err := NewRequest(method, url, header, body)
	if err != nil {
		return nil, err
	}

	return f.Do(req)
}

func NewFetcher(defaultHeader http.Header, clientPool *clientPool) *fetcher {
	if clientPool == nil {
		clientPool = DefaultClientPool
	}
	return &fetcher{
		header:     defaultHeader,
		clientPool: clientPool,
	}
}

// public methods
var DefaultFetcher *fetcher

func SetDefaultHeader(header http.Header) {
	DefaultFetcher.SetDefaultHeader(header)
}

// 使用默认Fetcher进行http访问
func Do(req *http.Request) (*http.Response, error) {
	return DefaultFetcher.Do(req)
}

// 使用默认Fetcher进行http访问
func Fetch(method, url string, header http.Header, body io.Reader) (*http.Response, error) {
	return DefaultFetcher.Fetch(method, url, header, body)
}
