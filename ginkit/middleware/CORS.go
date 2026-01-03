package middleware

import (
	"net/http"

	"github.com/Hana-ame/twitter-pic-go/Tools/utils"
	"github.com/gin-gonic/gin"
)

// CORS 中间件
func CORS() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 设置 CORS 头
		c.Header("Access-Control-Allow-Origin", utils.Or(c.Request.Header.Get("Origin"), "*")) // 或者指定特定的源
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD")
		c.Header("Access-Control-Allow-Headers", c.GetHeader("access-control-request-headers"))
		c.Header("Access-Control-Allow-Credentials", "true") // 允许cookie传递

		c.Header("Access-Control-Expose-Headers", "*") // 放这里可以吗？

		// 处理预检请求
		if c.Request.Method == http.MethodOptions {
			c.AbortWithStatus(http.StatusNoContent) // 返回 204 No Content
			return
		}

		c.Next() // 继续处理请求

		// 需要 override 掉的
		c.Header("cross-origin-resource-policy", "cross-origin")
	}
}
