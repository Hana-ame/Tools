package sqlite

import (
	"database/sql"
	"fmt"

	// _ "github.com/mattn/go-sqlite3" // SQLite 驱动
	_ "github.com/glebarez/go-sqlite"
)

func NewSQLiteDB(dbPath string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("无法打开数据库文件: %w", err)
	}

	// 尝试连接并验证数据库是否可用
	if err = db.Ping(); err != nil {
		db.Close() // 确保关闭连接
		return nil, fmt.Errorf("数据库连接失败: %w", err)
	}

	return db, nil
}
