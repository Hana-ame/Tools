package utils


// 用法同 a || b
func Or[T comparable](e ...T) T {
	var defaultValue T
	for _, v := range e {
		if v == defaultValue {
			continue
		} else {
			return v
		}
	}
	return defaultValue
}
