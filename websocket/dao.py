import sqlite3
from contextlib import closing


class SQLite3Resources:
    def __init__(self, fn="example.db"):
        self.conn = sqlite3.connect(fn)
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS resources (
                    id TEXT PRIMARY KEY,
                    preview_url TEXT NOT NULL,
                    url TEXT NOT NULL,
                    status_id TEXT NOT NULL DEFAULT ""
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS post_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键（INTEGER类型 + AUTOINCREMENT）[1,2,4](@ref)
                    thread_id INTEGER NOT NULL DEFAULT 0, -- 数字类型，非空，默认值0 [6,7](@ref)
                    status_id TEXT NOT NULL DEFAULT '',    -- 字符串类型，非空，默认空字符串 [7](@ref)
                    contents TEXT NOT NULL DEFAULT ''      -- 新增字段，非空，默认空字符串 [7](@ref)
                );
                """
            )
        self.conn.commit()

    def insert_on_conflict(self, id: str, preview_url: str, url: str, status_id: str):
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    """
                    INSERT INTO resources (id, preview_url, url, status_id)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        preview_url = excluded.preview_url,
                        url = excluded.url,
                        status_id = excluded.status_id
                    """,
                    (id, preview_url, url, status_id),
                )
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"更新失败: {e}")

    def select(self, id: str) -> tuple:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT * FROM resources WHERE id = ?", (id,))
            result = cursor.fetchone()
            if result:
                return result
            raise ValueError(f"ID {id} 不存在")

    def select_by_url(self, url: str) -> tuple:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT * FROM resources WHERE url = ?", (url,))
            result = cursor.fetchone()
            if result:
                return result
            raise ValueError(f"URL {url} 不存在")

    def patch(self, id: str, preview_url: str, url: str):
        _, _preview_url, _url = self.select(id)
        preview_url = preview_url or _preview_url
        url = url or _url
        self.insert_on_conflict(id, preview_url, url)

    def execute(self, sql: str, params: tuple = ()):
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    sql,
                    params,
                )
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"查询失败: {e}")

    def create_post_info(self, contents: str):
        self.execute(
            """
            INSERT INTO post_info (contents)
            VALUES (?);
            """,
            (contents,),
        )

    def update_post_info(self, thread_id: int, status_id: str, contents: str, id: int):
        self.execute(
            """
            UPDATE post_info SET
                thread_id = ?,
                status_id = ?,
                contents = ?
            WHERE id = ?
            """,
            (thread_id, status_id, contents, id),
        )

    def get_url(self, id_url: str):
        id, url = id_url.split("|", 1)
        result: tuple[str, str, str, str] = self.select(id)
        return result[2] or url

    def __del__(self):
        self.conn.close()  # 自动关闭连接


if __name__ == "__main__":
    dao = SQLite3Resources()
    try:
        print(dao.select("id"))  # 测试查询
    except Exception:
        pass
    dao.insert_on_conflict("id", "33", "43", "")
    try:
        print(dao.select("id"))  # 测试查询
    except Exception:
        pass
