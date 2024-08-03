package tools

import (
	"encoding/json"
	"fmt"
	"reflect"
	"testing"

	"github.com/Hana-ame/neo-moonchan/Tools/orderedmap"
)

func TestXxx(t *testing.T) {
	j := `{"a":["a","b"]}`
	o := orderedmap.New()
	json.Unmarshal([]byte(j), &o)
	fmt.Printf("%+v\n", o)
	sss := ParseSliceToStringSlice(o.Get("a"))
	fmt.Printf("%+v", sss)

}

func TestCast(t *testing.T) {
	var a any = "1"
	var b any = 1
	ta := reflect.TypeOf(a)
	tb := reflect.TypeOf(b)
	va := reflect.ValueOf(a)

	fmt.Printf("%+v\n", ta)
	fmt.Printf("%+v\n", tb)
	fmt.Printf("%+v\n", va)

}

func TestDef(t *testing.T) {
	var o any = nil
	m := orderedmap.New()
	m.Set("123", 321)
	o = Default(*m, orderedmap.New())
	fmt.Printf("%+v\n", o)
}

func TestOrderedmap(t *testing.T) {
	o := orderedmap.New()
	o.Set("application", o)
	fmt.Println(o)
	// var oa *orderedmap.OrderedMap
	oa := o.GetOrDefault("application", orderedmap.New()).(*orderedmap.OrderedMap)
	fmt.Println(oa)
}

func TestFromMap(t *testing.T) {
	m := map[string]any{
		"asdf": 123,
		"234":  4,
	}
	o := orderedmap.NewFromMap(m)
	var v any
	v = o.GetOrDefault("asdf", 1)
	fmt.Println(v)
	v = o.GetOrDefault("234", 1)
	fmt.Println(v)
	v = o.GetOrDefault("2345", 1)
	fmt.Println(v)
	fmt.Println(o)
}

func TestMarshalNil(t *testing.T) {
	var o *orderedmap.OrderedMap
	s, e := json.Marshal(o)
	fmt.Println(s, e)
	fmt.Println(string(s)) // null
}

func TestUnmarshalNil(t *testing.T) {
	s := "null"
	o := orderedmap.New()
	o.Set("key", "value")
	json.Unmarshal([]byte(s), o)
	fmt.Println(o) // same as orderedmap.New()
}

func TestUnmarshalPointer(t *testing.T) {
	s := `{"a": "b", "b":{"c": "d"} } `
	// s := `{a:"b"}`
	o := orderedmap.New()
	// fmt.Println(json.Unmarshal([]byte(s), *o)) // 这个不行，其他都可以
	// fmt.Println(o)
	fmt.Println(json.Unmarshal([]byte(s), o))
	fmt.Println(o)
	fmt.Println(json.Unmarshal([]byte(s), &o))
	fmt.Println(o)
	po := &o
	fmt.Println(json.Unmarshal([]byte(s), &(po)))
	fmt.Println(o)
}

// 全然大丈夫です
func TestUnmarshalSlice(t *testing.T) {
	s := `[{"b":"a"},{"a":"b"}]`
	// o := orderedmap.New()
	so := make([]*orderedmap.OrderedMap, 0, 5)
	fmt.Println(json.Unmarshal([]byte(s), &so))
	fmt.Println(so)
	for _, o := range so {
		fmt.Println(o)
	}
}
