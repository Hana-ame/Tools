package tools

import (
	"testing"

	"github.com/Hana-ame/azure-go/Tools/orderedmap"
)

func TestWriteJSON(t *testing.T) {
	o := orderedmap.New()
	o.Set("1", []int{1, 2, 3})
	WriteJSONToFile("test.json", o)
}
