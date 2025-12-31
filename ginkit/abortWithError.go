package ginkit

import "github.com/gin-gonic/gin"

func AbortWithError(c *gin.Context, code int, err error) bool {
	if err != nil {
		c.Header("X-Error", err.Error())
		c.AbortWithStatusJSON(code, gin.H{
			"error": err.Error(),
		})
		return true
	}
	return false
}
