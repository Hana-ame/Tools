package tools

import (
	"fmt"
	"testing"
)

func TestTimestamp(t *testing.T) {
	a := Now()
	fmt.Println(a)
}
