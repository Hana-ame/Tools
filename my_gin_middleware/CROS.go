package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// CORS 中间件
func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 设置 CORS 头
		c.Header("Access-Control-Allow-Origin", c.Request.Header.Get("Origin")) // 或者指定特定的源
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD")
		c.Header("Access-Control-Allow-Headers", "Content-Type")

		// 处理预检请求
		if c.Request.Method == http.MethodOptions {
			c.AbortWithStatus(http.StatusNoContent) // 返回 204 No Content
			return
		}

		c.Next() // 继续处理请求
	}
}

// func main() {
// 	router := gin.Default()

// 	// 使用 CORS 中间件
// 	router.Use(CORSMiddleware())

// 	// 定义路由
// 	router.GET("/example", func(c *gin.Context) {
// 		c.JSON(http.StatusOK, gin.H{"message": "Hello, World!"})
// 	})

// 	// 启动服务器
// 	router.Run(":8080")
// }
