package tools

type FuncWrapper[T any] func() (T, error)

func (w *FuncWrapper[T]) DefautValue(defaultValue T) T {
	v, e := (*w)()
	if e != nil {
		return defaultValue
	}
	return v
}

// 用法同 a || b
func Or[T comparable](e, d T) T {
	var defaultValue T
	if e == defaultValue {
		return d
	}
	return e
}

// 是不是用不了。
// func And[T any](a any, d T) T {
// 	if a == nil {
// 		return d
// 	}
// 	return a.(T)
// }
