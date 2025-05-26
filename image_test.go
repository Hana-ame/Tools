// gemini

package tools

import (
	"fmt"
	"log"
	"net/http"
	"testing"
)

func TestRespToImg(t *testing.T) {
	// This is a placeholder. In a real scenario, you'd get an *http.Response
	// from an http.Get or similar.
	// For example, to test, you could set up a mock server or fetch a real image.

	// Example: Fetching a known WebP image (replace with a real URL if testing)
	resp, err := http.Get("https://www.gstatic.com/webp/gallery/1.webp")
	if err != nil {
		log.Fatalf("Failed to get image: %v", err)
	}

	img, err := DecodeResponseToImage(resp)
	if err != nil {
		log.Fatalf("Failed to decode image: %v", err)
	}

	fmt.Printf("Successfully decoded image. Dimensions: %s\n", img.Bounds())
}
