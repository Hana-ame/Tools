package main

import (
	examples "github.com/hana-ame/udptun/Tools/ws_mux/examples"
)

func main() {
	for {
		examples.UploadFileBySha1sum("wss://file.moonchan.xyz/ws/server", nil)
	}
}
