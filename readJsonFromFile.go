// azure-go @ 2023-12-21

package tools

import (
	"encoding/json"
	"os"

	"github.com/Hana-ame/neo-moonchan/Tools/orderedmap"
)

// this function receive json request.
func ReadJsonFromFile(fn string) (*orderedmap.OrderedMap, error) {
	jsonFile, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	o := orderedmap.New()
	err = json.NewDecoder(jsonFile).Decode(&o)
	return o, err
}
