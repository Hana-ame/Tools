// @241015

package mycurl

import (
	"bytes"
	"fmt"
	"io"
	"os/exec"
	"strconv"
)

type Header struct {
	Key   string
	Value string
}

func (h *Header) String() string {
	return h.Key + ": " + h.Value
}

type Headers []*Header

func Curl(method string, agent string, headers Headers, cookie string, url string, bodyReader io.ReadCloser, argv ...string) (statusCode int, body []byte, err error) {
	argv = append(argv, "-X", method)
	if agent != "" {
		argv = append(argv, "-A", agent)
	}

	if bodyReader != nil {
		body, err = io.ReadAll(bodyReader)
		if err != nil {
			return
		}
	}
	for _, header := range headers {
		argv = append(argv, "-H", header.String())
	}
	if cookie != "" {
		argv = append(argv, "-d", cookie)
	}

	argv = append(argv, url)

	return curl(argv...)
}

func curl(argv ...string) (statusCode int, body []byte, err error) {
	var stderr bytes.Buffer
	argv = append(argv, "-w", "%{http_code}", "-s")

	cmd := exec.Command("curl", argv...)

	// 将stderr设置为我们创建的Buffer
	cmd.Stderr = &stderr

	// 执行命令并获取输出
	body, err = cmd.Output()
	if err != nil {
		return
	}
	statusCode, err = strconv.Atoi(string(body[len(body)-3:]))
	if err != nil {
		return
	}
	errstr := stderr.String()
	if len(errstr) > 0 {
		err = fmt.Errorf("%s", errstr)
	}
	// 打印正常输出
	return statusCode, body[:len(body)-3], err

}
