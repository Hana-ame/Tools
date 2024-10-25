package handlerFunc

import (
	"io"
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

func Proxy(targetUrl, path string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// 创建目标 URL
		target, _ := url.Parse(targetUrl)

		// 创建请求
		proxy := c.Request.Clone(c.Request.Context())
		proxy.URL.Scheme = target.Scheme
		proxy.URL.Host = target.Host
		proxy.URL.Path = path
		proxy.Host = target.Host

		// 发送请求到目标服务器
		client := &http.Client{}
		resp, err := client.Do(proxy)
		if err != nil {
			c.String(http.StatusBadGateway, "Bad Gateway")
			return
		}
		defer resp.Body.Close()

		// 设置响应头和状态码
		for key, value := range resp.Header {
			c.Header(key, value[0])
		}
		c.Status(resp.StatusCode)

		// 流式传输响应数据
		_, err = io.Copy(c.Writer, resp.Body)
		if err != nil {
			c.String(http.StatusInternalServerError, "Error copying response body")
		}
	}
}
