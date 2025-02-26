package tools

func NewFuncWrapper[T any](result T, err error) *FuncWrapper[T] {
	return &FuncWrapper[T]{
		result: result,
		err:    err,
	}
}

type FuncWrapper[T any] struct {
	result T
	err    error
}

func (w *FuncWrapper[T]) Then(handler func(result T)) *FuncWrapper[T] {
	if w.err == nil {
		handler(w.result)
	}
	return w
}

func (w *FuncWrapper[T]) Catch(handler func(err error)) *FuncWrapper[T] {
	handler(w.err)
	return w
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

// catch一个单输出+error的function，并且
// 返回一个result，result有几个方法，可以在一行里面处理
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

func (r *result[T]) Result() T {
	return r.result
}

func (r *result[T]) Error() error {
	return r.err
}
