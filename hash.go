// antenna @ 2024-01-05
// azure-go @ 2023-12-21

package tools

import (
	"crypto/sha256"
	"fmt"
)

func Hash(s string, SALT string) string {
	hash := sha256.Sum256([]byte(s + SALT))
	hashString := fmt.Sprintf("%x", hash)
	return hashString
}
