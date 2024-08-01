package tools

import (
	"encoding/json"
	"fmt"
	"reflect"
	"testing"

	"go-tools/Tools/orderedmap"
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
