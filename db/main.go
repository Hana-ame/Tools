// usage:
// 把一个只返回err的handler function传进来。
// TODO:
// 这里db每次open close肯定不对的。

package db

import (
	"database/sql"
	"os"

	_ "github.com/joho/godotenv/autoload"
	_ "github.com/lib/pq"
)

func Exec(handler func(tx *sql.Tx) error) error {
	connStr := os.Getenv("CONN_STR")
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return err
	}
	defer db.Close()

	tx, err := db.Begin()
	if err != nil {
		return err
	}

	// 如果handler当中不Commit那么就会统一Rollback
	defer tx.Rollback()

	return handler(tx)
}
