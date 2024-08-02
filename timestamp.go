package tools

import "time"

func Now() int64 {
	now := time.Now()
	timestamp := now.UnixNano()
	return timestamp * 65536 / 1e9
}
