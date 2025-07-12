package tools

import (
	"os/exec"
)

func Command(name string, arg ...string) (string, error) {
	cmd := exec.Command(name, arg...)
	// 捕获输出
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}
	return string(output), nil
}
