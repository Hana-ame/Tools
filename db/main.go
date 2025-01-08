package db

import (
	"database/sql"
	"os"

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

	return handler(tx)

}
