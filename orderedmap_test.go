package tools

import (
	"encoding/json"
	"fmt"
	"testing"

	"github.com/Hana-ame/orderedmap"
)

func TestXxx(t *testing.T) {
	j := `{"a":["a","b"]}`
	o := orderedmap.New()
	json.Unmarshal([]byte(j), &o)
	fmt.Printf("%+v\n", o)
	sss := ParseSliceToStringSlice(o.Get("a"))
	fmt.Printf("%+v", sss)

}
