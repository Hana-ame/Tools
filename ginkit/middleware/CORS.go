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
		// 保留 Origin 反射：跨域前端依赖它。
		// 已删除 Access-Control-Allow-Credentials: 全项目无 Cookie / 认证头鉴权，
		// 反射 Origin + credentials 等于让任意站点发带凭证跨域请求。
		c.Header("Access-Control-Allow-Origin", utils.Or(c.Request.Header.Get("Origin"), "*"))
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD")
		// 不要回显请求头：任何请求头都能被反射到响应里，扩大了攻击面。
		// 改成前端确实会用到的固定清单。
		c.Header("Access-Control-Allow-Headers", "Content-Type, Accept, X-Requested-With")
		// 已删除 Access-Control-Expose-Headers: *：它让任意域能读响应头里的
		// X-Error（abortWithError 曾把原始 SQL / 路径错误写进这个头）。
		// 前端也没有依赖任何自定义响应头，故干脆不设。

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
