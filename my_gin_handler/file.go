// 24-09-21 @ gin-pack

package handler

import (
	"crypto/sha1"
	"encoding/hex"
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

// UploadFiles 处理文件上传并将文件保存到 /uploads/[sha1sum]/[filename]
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
		// 计算文件的 SHA1 校验和
		fileContent, err := file.Open()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "打开文件失败: " + err.Error()})
			return
		}
		defer fileContent.Close()

		hasher := sha1.New()
		if _, err := io.Copy(hasher, fileContent); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "计算 SHA1 失败: " + err.Error()})
			return
		}

		// 获取 SHA1 值并生成新的文件夹路径
		sha1sum := hex.EncodeToString(hasher.Sum(nil))
		dirPath := path.Join("uploads", sha1sum) // 使用 SHA1 值作为文件夹名

		// 创建目录
		if err := os.MkdirAll(dirPath, os.ModePerm); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "创建目录失败: " + err.Error()})
			return
		}

		// 保存文件
		savePath := path.Join(dirPath, file.Filename) // 完整的文件保存路径
		if err := c.SaveUploadedFile(file, savePath); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "保存文件失败: " + err.Error()})
			return
		}

		savedFiles = append(savedFiles, savePath)
	}

	// 返回成功响应
	c.JSON(http.StatusOK, gin.H{"message": "文件上传成功", "files": savedFiles})
}
