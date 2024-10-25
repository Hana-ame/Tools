// azure-go @ 2023-12-21

package tools

import (
	"encoding/json"
	"os"

	"github.com/Hana-ame/fedi-antenna/Tools/orderedmap"
)

// this function receive json request.
func ReadJsonFile(fn string) (*orderedmap.OrderedMap, error) {
	jsonFile, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	o := orderedmap.New()
	err = json.NewDecoder(jsonFile).Decode(&o)
	return o, err
}
