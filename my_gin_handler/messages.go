package handler

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	tools "github.com/Hana-ame/neo-moonchan/Tools"
	"github.com/Hana-ame/neo-moonchan/Tools/db"
	"github.com/Hana-ame/neo-moonchan/Tools/orderedmap"
	"github.com/gin-gonic/gin"
)

type message struct {
	ID       int                    `json:"id"`
	Receiver string                 `json:"receiver"`
	Sender   string                 `json:"sender"`
	Payload  *orderedmap.OrderedMap `json:"payload"`
}

// :receiver
func SendMsg(c *gin.Context) {
	receiver := tools.NewSlice[string](c.GetString("receiver"), c.Param("receiver"), c.Query("receiver")).FirstNonDefaultValue("")
	sender := tools.NewSlice[string](c.GetString("sender"), c.Param("sender"), c.Query("sender"), c.GetHeader("X-Forwarded-For")).FirstNonDefaultValue("")

	if err := db.Exec(func(tx *sql.Tx) error {
		query := `INSERT INTO messages (id, receiver, sender, payload) VALUES ($1, $2, $3, $4);`
		id := tools.NewTimeStamp()
		blob, err := c.GetRawData()
		if err != nil {
			return err
		}
		if _, err := tx.Exec(query, id, receiver, sender, blob); err != nil {
			return err
		}
		return tx.Commit()
	}); err != nil {
		c.Header("X-Error", err.Error())
		c.AbortWithStatus(http.StatusInternalServerError)
	}

	c.AbortWithStatus(http.StatusNoContent)
}

// :receiver
// ?after
// ?limit
func ReceiveMsg(c *gin.Context) {
	receiver := tools.NewSlice[string](c.GetString("receiver"), c.Param("receiver"), c.Query("receiver")).FirstNonDefaultValue("")
	afterString := tools.NewSlice[string](c.GetString("after"), c.Param("after"), c.Query("after")).FirstNonDefaultValue("")
	after, err := strconv.Atoi(afterString)
	if err != nil {
		after = 0
	}
	limitString := tools.NewSlice[string](c.GetString("limit"), c.Param("limit"), c.Query("limit")).FirstNonDefaultValue("")
	limit, err := strconv.Atoi(limitString)
	if err != nil {
		limit = 10
	}
	if limit <= 0 || limit > 100 {
		limit = 10
	}

	messages := make([]message, 0, limit) // Initialize with capacity, not length

	if err := db.Exec(func(tx *sql.Tx) error {
		rows, err := tx.Query("SELECT id, receiver, sender, payload FROM messages WHERE receiver = $1 AND id > $2 ORDER BY id ASC LIMIT $3", receiver, after, limit)
		if err != nil {
			return err
		}
		defer rows.Close()

		for rows.Next() {
			var msg message
			var blob []byte
			if err := rows.Scan(&msg.ID, &msg.Receiver, &msg.Sender, &blob); err != nil {
				return err
			}
			if err := json.Unmarshal(blob, &msg.Payload); err != nil {
				return err
			}

			messages = append(messages, msg)
		}
		if err := rows.Err(); err != nil {
			return err
		}

		return tx.Commit()
	}); err != nil {
		c.Header("X-Error", err.Error())
		c.AbortWithStatus(http.StatusInternalServerError)
	}

	c.JSON(http.StatusOK, messages)
}
