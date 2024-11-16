package tools

import (
	"time"
)

func Now() int64 {
	ts := (((time.Now().UnixNano()) / 100_000) << 16) / 10
	return (int64(ts))
}
