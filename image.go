package tools

import (
	"fmt"
	"image"
	"image/gif"
	"image/jpeg"
	"image/png"
	"net/http"

	"github.com/mat/besticon/v3/ico"
)

// https://github.com/buckket/go-blurhash
// for image encode to blurhash

func DecodeResponseToImage(r *http.Response) (image.Image, error) {
	switch r.Header.Get("Content-Type") {
	case "image/x-icon":
		return ico.Decode(r.Body)
	case "image/jpeg":
		return jpeg.Decode(r.Body)
	case "image/png":
		return png.Decode(r.Body)
	case "image/gif":
		return gif.Decode(r.Body)
	default:
		return nil, fmt.Errorf("not supported yed")
	}
}

// func Read
