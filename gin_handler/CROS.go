package handler

import "github.com/gin-gonic/gin"

// CORSMiddleware 添加CORS头，允许跨域请求携带cookie
func CORSMiddleware(host string) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", host) // 允许特定的前端地址
		c.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
		c.Header("Access-Control-Allow-Headers", "Origin, Content-Type, Accept, Authorization")
		c.Header("Access-Control-Allow-Credentials", "true") // 允许cookie传递

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			// return // 应该不用这句
		}

		c.Next()
	}
}
