// azure-go @ 2023-12-21

package myiter

import (
	"fmt"
	"testing"

	"github.com/Hana-ame/orderedmap"
)

// pass an iter function to iter then you can iter it.
func TestX(t *testing.T) {
	o := orderedmap.New()
	o.Set("a", "11")
	o.Set("b", "22")
	o.Set("c", "33")
	iter := NewIter(o)
	i := "00"
	f := func(k, v any) bool {
		fmt.Println(k, v)
		i += v.(string)
		return false
	}
	iter.Iter(f)
	fmt.Println(i)
}

func TestS(t *testing.T) {
	o := []int{1, 2, 3, 4, 5}
	iter := NewIter(o)
	i := 0
	f := func(k, v any) bool {
		fmt.Println(k, v)
		i += v.(int)
		return false
	}
	iter.Iter(f)
	fmt.Println(i)
}

/*
	it don't support types. that's really silly.
*/
