package mycurl

import (
	"bytes"
	"fmt"
	"os/exec"
	"testing"
)

func TestCurl(t *testing.T) {
	code, body, err := curl("https://google.com")
	fmt.Println(err)
	fmt.Println(string(body))
	fmt.Println(code)
}

func TestCurl2(t *testing.T) {
	headers := Headers{
		&Header{
			Key:   "21",
			Value: "21",
		},
		&Header{
			Key:   "121",
			Value: "212",
		},
	}
	cookie := ""
	code, body, err := Curl("GET", headers, cookie, "https://getip.moonchan.xyz/echo/1", nil)
	fmt.Println(err)
	fmt.Println(string(body))
	fmt.Println(code)
}

func TestXxx(t *testing.T) {
	var stderr bytes.Buffer
	// 定义要执行的curl命令
	cmd := exec.Command("curl", "-s", "-w", "%{http_code}", "https://1google.com") // 使用一个无效的URL来模拟错误

	// 将stderr设置为我们创建的Buffer
	cmd.Stderr = &stderr

	// 执行命令并获取输出
	output, err := cmd.Output()
	// if err != nil {
	// 如果有错误，打印错误信息
	fmt.Println("错误:", err)
	fmt.Println("标准错误输出:", stderr.String())
	// return
	// }

	// 打印正常输出
	fmt.Println(string(output))

}
