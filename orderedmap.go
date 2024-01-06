package tools

// return &s
func ParsePointerToString(s any, ok bool) string {
	if !ok {
		return ""
	}
	if s == nil {
		return ""
	}
	switch v := s.(type) {
	case string:
		return v
	case *string:
		return *v
	}
	return ""
}

// return &s
func ParseSliceToStringSlice(s any, ok bool) []string {
	if !ok {
		return nil
	}
	if s == nil {
		return nil
	}
	switch v := s.(type) {
	case []any:
		ss := make([]string, len(v))
		for i, s := range v {
			ss[i] = s.(string)
		}
		return ss
	}
	return nil
}
