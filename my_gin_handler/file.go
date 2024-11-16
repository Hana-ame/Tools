// 24-09-21 @ gin-pack

package handler

import (
	"io"
	"log"
	"net/http"
	"os"
	"path"

	"github.com/gin-gonic/gin"
)

// servefile
func FileHandler(filepath func() string) func(c *gin.Context) {
	return func(c *gin.Context) {
		ip := c.GetHeader("CF-Connecting-IP")
		log.Println(ip)
		c.File(filepath())
	}
}

func UploadFile(c *gin.Context) {
	file, err := os.Create("upload/file.txt")
	if err != nil {
		c.JSON(500, gin.H{
			"message": "创建文件失败",
		})
		return
	}
	defer file.Close()

	_, err = io.Copy(file, c.Request.Body)
	if err != nil {
		c.JSON(500, gin.H{
			"message": "写入文件失败",
		})
		return
	}

	c.JSON(200, gin.H{
		"message": "文件上传成功",
	})
}

// by gpt, not reviewed.
func UploadFiles(c *gin.Context) {
	// 获取所有上传的文件
	form, err := c.MultipartForm()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "获取文件失败: " + err.Error()})
		return
	}

	// 获取文件列表
	files := form.File["files"] // "files" 是表单中 file input 的 name 属性，可以包含多个文件

	var savedFiles []string

	// 遍历文件并保存
	for _, file := range files {
		// 指定保存路径
		savePath := path.Join("uploads", file.Filename)

		// 保存文件
		if err := c.SaveUploadedFile(file, savePath); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "保存文件失败: " + err.Error()})
			return
		}

		savedFiles = append(savedFiles, savePath)
	}

	// 返回成功响应
	c.JSON(http.StatusOK, gin.H{"message": "文件上传成功", "files": savedFiles})
}
