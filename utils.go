package tools

func Restrict(value, min, max int) int {
	switch {
	case value > max:
		return max
	case value < min:
		return min
	default:
		return value
	}
}
