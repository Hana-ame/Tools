package main

import (
	examples "github.com/Hana-ame/neo-moonchan/Tools/ws_mux/examples"
)

func main() {
	for {
		examples.UploadFileBySha1sum("wss://file.moonchan.xyz/ws/server", nil)
	}
}
