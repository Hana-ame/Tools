// azure-go @ 2023-12-21

package tools

import (
	"bytes"
	"encoding/json"
	"io"
	"os"
	"strings"

	"github.com/Hana-ame/udptun/Tools/orderedmap"
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

func ReaderToJson(reader io.Reader) (*orderedmap.OrderedMap, error) {
	o := orderedmap.New()
	err := json.NewDecoder(reader).Decode(&o)
	return o, err
}

func StringToJson(s string) (*orderedmap.OrderedMap, error) {
	return ReaderToJson(strings.NewReader(s))
}

func BytesToJson(b []byte) (*orderedmap.OrderedMap, error) {
	return ReaderToJson(bytes.NewReader(b))
}

func ReadFileToJson(fn string) (*orderedmap.OrderedMap, error) {
	f, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	return ReaderToJson(f)
}
