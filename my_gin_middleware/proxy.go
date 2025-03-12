package middleware

import (
	"net/http"
	"net/url"

	tools "github.com/Hana-ame/api-pack/Tools"
	myfetch "github.com/Hana-ame/api-pack/Tools/my_fetch"
	"github.com/gin-gonic/gin"
)

// 必须设置 X-Scheme 开启功能, 只支持 X-Host... 方式的设置
func ProxyMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {

		scheme := c.GetHeader("X-Scheme")

		if scheme != "" {

			requestURL := c.Request.URL.String()

			host := c.GetHeader("X-Host")
			origin := c.GetHeader("X-Origin")
			referer := c.GetHeader("X-Referer")

			href, err := url.Parse(requestURL)
			if err != nil {
				c.Header("X-Error", err.Error())
				c.AbortWithError(http.StatusInternalServerError, err)
				return
			}
			href.Host = host
			href.Scheme = scheme

			hrefString := href.String()

			header := tools.NewHeader(c.Request.Header)

			header.Set("Host", host)
			header.Set("Origin", origin)
			header.Set("Referer", referer)
			header.Set("Cookie", tools.Or(c.GetHeader("X-Cookie"), header.Get("Cookie")))

			resp, err := myfetch.Fetch(c.Request.Method, hrefString,
				(header.Header), c.Request.Body)
			if err != nil {
				c.Header("X-Error", err.Error())
				c.AbortWithError(http.StatusBadGateway, err)
				return
			}
			defer resp.Body.Close()

			// 为什么自带的方法这么贵物
			for k, vs := range resp.Header {
				if c.Writer.Header().Get(k) != "" { // 擦,好像是因为自己改了什么ContentType所以不好直接弄.但是还是保留了吧.
					continue
				}
				for _, v := range vs {
					c.Writer.Header().Add(k, v)
				}
			}
			// slices.Sort(exposeHeaders)
			// c.Writer.Header().Add("Access-Control-Expose-Headers", strings.Join(exposeHeaders, ", "))

			c.DataFromReader(resp.StatusCode, resp.ContentLength, resp.Header.Get("Content-Type"), resp.Body, map[string]string{
				"X-Host":    host,
				"X-Origin":  header.Get("Origin"),
				"X-Referer": header.Get("Referer"),
				"X-Cookie":  header.Get("Cookie"),
				"X-Href":    hrefString,
			})

			return
		}

		// 否则不处理
		c.Next()
	}
}
