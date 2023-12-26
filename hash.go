// azure-go @ 2023-12-21

package tools

import (
	"crypto/sha256"
	"fmt"
)

func hash(s string, SALT string) string {
	hash := sha256.Sum256([]byte(s + SALT))
	hashString := fmt.Sprintf("%x", hash[:2])
	return hashString
}
