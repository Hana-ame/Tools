package tools

import "fmt"

type Slice[T comparable] []T

func NewSlice[T comparable](e ...T) Slice[T] {
	return Slice[T](e)
}

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

func (s Slice[T]) Last(defaultValue ...T) T {
	if len(s) == 0 {
		if len(defaultValue) == 0 {
			var dv T
			return dv
		}
		return defaultValue[0]
	}
	return s[len(s)-1]
}

// func (s Slice[T]) Push(e T) Slice[T] {
// 	s = append(s, e)
// 	return s
// }

// func (s Slice[T]) Pop() (Slice[T], T) {
// 	e := s.Last()
// 	s = s[:len(s)-1]
// 	return s, e
// }

func (s Slice[T]) FirstUnequal(v T) T {
	for _, e := range s {
		if e != v {
			return e
		}
	}
	return v
}

// func (s Slice[T]) First(filter func(v T) bool, defaultValue T) (T, error) {
// 	for _, v := range s {
// 		if filter(v) {
// 			return v, nil
// 		}
// 	}
// 	return defaultValue, fmt.Errorf("null")
// }

func (s Slice[T]) First(defaultValue T) T {
	if len(s) == 0 {
		return defaultValue
	}
	return s[0]
}

//	func (s Slice[T]) Map(index i[RT any]nt, defaultValue T) RT {
//		if index < 0 || len(s) >= index {
//			return defaultValue
//		}
//		return s[index]
//	}
func (s Slice[T]) Filter(filter func(v T) bool) Slice[T] {
	result := make([]T, 0, len(s))
	for _, v := range s {
		if filter(v) {
			result = append(result, v)
		}
	}

	return result
}

func MoveToFirstInPlace[T comparable](arr []T, target T) {
	for i, v := range arr {
		if v == target && i != 0 {
			// 将目标元素冒泡到首位
			for j := i; j > 0; j-- {
				arr[j], arr[j-1] = arr[j-1], arr[j]
			}
			return
		}
	}
}

func UnEqual[T comparable](values ...T) func(v T) bool {
	return func(v T) bool {
		for _, value := range values {
			if v == value {
				return false
			}
		}
		return true
	}
}
