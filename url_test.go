package tools

import (
	"fmt"
	"net/url"
	"testing"
)

func TestURLParams(t *testing.T) {
	// 解析原始 URL
	rawURL := "/path?foo=bar"
	parsedURL, err := url.Parse(rawURL)
	if err != nil {
		fmt.Println("Error parsing URL:", err)
		return
	}

	// 添加参数
	query := parsedURL.Query()
	query.Set("baz", "qux")             // 添加或更新参数
	parsedURL.RawQuery = query.Encode() // 更新 URL 的查询部分

	// 输出修改后的 URL
	fmt.Println("Updated URL:", parsedURL.String())

}
