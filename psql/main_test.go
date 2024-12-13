package psql

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"testing"

	_ "github.com/joho/godotenv/autoload"

	_ "github.com/lib/pq"
)

func TestConnection(t *testing.T) {
	connStr := os.Getenv("CONN_STR")

	for i := 0; i < 200; i++ {
		// 连接到 PostgreSQL 数据库
		db, err := sql.Open("postgres", connStr)
		if err != nil {
			log.Fatal("Error connecting to the database: ", err)
		}
		defer db.Close()

		// 测试连接
		err = db.Ping()
		if err != nil {
			log.Fatal("Error pinging the database: ", err)
		}
		fmt.Println("Successfully connected to the database!")

		fmt.Printf("%v", db)
	}
}
