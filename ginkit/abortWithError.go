package ginkit

import (
	"log"

	"github.com/gin-gonic/gin"
)

// AbortWithError 统一错误响应。
// X-Error 头只写类别，不写原始错误内容：之前把 SQL / 路径等内部细节
// 原样塞进响应头，再叠加 CORS 的 Expose-Headers: * 等于任意站点都能读到。
// 细节只打到服务端日志。
func AbortWithError(c *gin.Context, code int, err error) bool {
	if err != nil {
		log.Printf("AbortWithError: status=%d err=%v", code, err)
		c.Header("X-Error", "error")
		c.AbortWithStatusJSON(code, gin.H{
			"error": err.Error(),
		})
		return true
	}
	return false
}