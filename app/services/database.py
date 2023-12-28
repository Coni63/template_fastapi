import sqlite3

from app.entities.todo import Todo


class Database:
    path_db = "database.sqlite"

    @staticmethod
    def setup_db():
        with sqlite3.connect(Database.path_db) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS todo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    state TEXT
                );
                """
            )
            conn.commit()

    @staticmethod
    def drop_db():
        with sqlite3.connect(Database.path_db) as conn:
            conn.execute(
                """
                DROP TABLE IF EXISTS todo;
                """
            )
            conn.commit()

    @staticmethod
    def get_all_items() -> list[Todo]:
        try:
            with sqlite3.connect(Database.path_db) as conn:
                cursor = conn.execute(
                    """
                    SELECT id, title, description, state
                    FROM todo;
                    """
                )
                return [
                    Todo(
                        id=row[0],
                        title=row[1],
                        description=row[2],
                        state=row[3],
                    )
                    for row in cursor.fetchall()
                ]
        except Exception:
            return []

    @staticmethod
    def get_item_by_id(id: int) -> Todo | None:
        try:
            with sqlite3.connect(Database.path_db) as conn:
                cursor = conn.execute(
                    """
                    SELECT id, title, description, state
                    FROM todo
                    WHERE id = ?;
                    """,
                    (id,),
                )
                row = cursor.fetchone()
                return Todo(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    state=row[3],
                )
        except Exception:
            return None

    @staticmethod
    def create_item(item: Todo) -> int:
        with sqlite3.connect(Database.path_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO todo (title, description, state)
                VALUES (?, ?, ?);
                """,
                (item.title, item.description, item.state),
            )
            return cursor.lastrowid

    @staticmethod
    def update_item(id: int, new_item: Todo):
        with sqlite3.connect(Database.path_db) as conn:
            conn.execute(
                """
                UPDATE todo
                SET title = ?, description = ?, state = ?
                WHERE id = ?;
                """,
                (new_item.title, new_item.description, new_item.state, id),
            )

    @staticmethod
    def delete_item(id: int):
        with sqlite3.connect(Database.path_db) as conn:
            conn.execute(
                """
                DELETE FROM todo
                WHERE id = ?;
                """,
                (id,),
            )
