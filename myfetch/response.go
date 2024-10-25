// timeline-deamon @ 2023-12-26
// azure-go @ 2023-12-21

package myfetch

import (
	"encoding/json"
	"net/http"

	"github.com/Hana-ame/udptun/Tools/orderedmap"
)

// this function receive json request.
func ResponseToObject(r *http.Response) (o *orderedmap.OrderedMap, err error) {
	o = orderedmap.New()
	err = json.NewDecoder(r.Body).Decode(&o)
	return o, err
}

func ResponseToObjectArray(r *http.Response) (arr []*orderedmap.OrderedMap, err error) {
	err = json.NewDecoder(r.Body).Decode(&arr)
	return arr, err
}
