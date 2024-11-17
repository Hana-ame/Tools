package tools

import (
	"encoding/json"
	"fmt"
	"testing"
)

func TestSlice(t *testing.T) {
	var s []int
	var js []byte
	s = nil
	fmt.Printf("%v\n", s) // []
	for k, v := range s { // ok
		fmt.Printf("%v, %v\n", k, v)
	}
	js, _ = json.Marshal(s)
	fmt.Printf("%s\n", js) // null

	s = []int{}
	fmt.Printf("%v\n", s) // []
	for k, v := range s { // ok
		fmt.Printf("%v, %v\n", k, v)
	}
	js, _ = json.Marshal(s)
	fmt.Printf("%s\n", js) // []

}
