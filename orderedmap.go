package tools

import (
	"reflect"

	"github.com/Hana-ame/neo-moonchan/Tools/orderedmap"
)

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

// 用不了的吧
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

func GetOrDefault(o *orderedmap.OrderedMap, key string, def any) any {
	v, ok := o.Get(key)
	if !ok {
		return def
	}
	if reflect.TypeOf(v) == reflect.TypeOf(def) {
		return v
	}
	return def

}

func Default(val, def any) any {
	if reflect.TypeOf(val) == reflect.TypeOf(def) {
		return val
	}
	return def
}
