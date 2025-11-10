import sqlite3

DB_FILE = "books.db"

def create_table():
    """建立 llm_books 資料表（若不存在）"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        conn.execute("""
        CREATE TABLE IF NOT EXISTS llm_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            author TEXT,
            price INTEGER,
            link TEXT
        );
        """)

def insert_books(books):
    """批量存入書籍資料，已存在的書名會被忽略"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        count = 0
        for b in books:
            cursor.execute("""
            INSERT OR IGNORE INTO llm_books (title, author, price, link)
            VALUES (?, ?, ?, ?)
            """, (b["title"], b["author"], b["price"], b["link"]))
            if cursor.rowcount > 0:
                count += 1
        conn.commit()
    return count

def query_books_by_title(keyword):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM llm_books WHERE title LIKE ?", (f"%{keyword}%",))
        return cursor.fetchall()

def query_books_by_author(keyword):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM llm_books WHERE author LIKE ?", (f"%{keyword}%",))
        return cursor.fetchall()
