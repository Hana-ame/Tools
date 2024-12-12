package tools

type FuncWrapper[T any] func() (T, error)

func (w *FuncWrapper[T]) DefautValue(defaultValue T) T {
	v, e := (*w)()
	if e != nil {
		return defaultValue
	}
	return v
}
