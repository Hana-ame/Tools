// azure-go @ 2023-12-21

// this function receive json request.
func readJsonFromFile(fn string) (*orderedmap.OrderedMap, error) {
	jsonFile, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	o := orderedmap.New()
	err = json.NewDecoder(jsonFile).Decode(&o)
	return o, err
}

