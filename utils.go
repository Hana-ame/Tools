package tools

import (
	"bytes"
	"fmt"
)

func Seprate(separator, data []byte) ([]byte, []byte, error) {
	// 查找 \r\n\r\n 的位置
	index := bytes.Index(data, separator)
	if index == -1 {
		err := fmt.Errorf("%s", data)
		return nil, nil, err
	}
	return data[:index], data[index+len(separator):], nil
}

type Slice[T any] []T

func (s Slice[T]) Get(index int) (T, error) {
	if index < 0 || index >= len(s) {
		var defaultValue T
		return defaultValue, fmt.Errorf("out of range")
	}
	return s[index], nil
}

func (s Slice[T]) GetOrDefault(index int, defaultValue T) T {
	if index < 0 || index >= len(s) {
		return defaultValue
	}
	return s[index]
}

// func (s Slice[T]) Map(index i[RT any]nt, defaultValue T) RT {
// 	if index < 0 || len(s) >= index {
// 		return defaultValue
// 	}
// 	return s[index]
// }

type FuncWrapper[T any] func() (T, error)

func (w *FuncWrapper[T]) DefautValue(defaultValue T) T {
	v, e := (*w)()
	if e != nil {
		return defaultValue
	}
	return v
}
