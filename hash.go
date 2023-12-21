// azure-go @ 2023-12-21


func hash(s string) string {
	hash := sha256.Sum256([]byte(s + agent.SALT))
	hashString := fmt.Sprintf("%x", hash[:2])
	return hashString
}

