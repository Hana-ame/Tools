// azure-go @ 2023-12-21

package tools

import (
	"bytes"
	"encoding/json"
	"io"
	"os"
	"strings"

	"github.com/Hana-ame/neo-moonchan/Tools/orderedmap"
)

// this function receive json request.
func ReadJSONFile(fn string) (*orderedmap.OrderedMap, error) {
	jsonFile, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	o := orderedmap.New()
	err = json.NewDecoder(jsonFile).Decode(&o)
	return o, err
}

func ReaderToJSON(reader io.Reader) (*orderedmap.OrderedMap, error) {
	o := orderedmap.New()
	err := json.NewDecoder(reader).Decode(&o)
	return o, err
}

func StringToJSON(s string) (*orderedmap.OrderedMap, error) {
	return ReaderToJSON(strings.NewReader(s))
}

func BytesToJSON(b []byte) (*orderedmap.OrderedMap, error) {
	return ReaderToJSON(bytes.NewReader(b))
}

func ReadFileToJSON(fn string) (*orderedmap.OrderedMap, error) {
	f, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	return ReaderToJSON(f)
}
