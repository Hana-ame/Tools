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

type result[T any] struct {
	result T
	err    error
	// defaultResult T
}

func Match[T any](r T, err error) *result[T] {
	return &result[T]{
		result: r,
		err:    err,
	}
}

func (r *result[T]) GetOrDefault(defaultValue T) T {
	if r.err != nil {
		return defaultValue
	}
	return r.result
}

func (r *result[T]) IgnoreError() T {
	return r.result
}

func (r *result[T]) Error() error {
	return r.err
}
