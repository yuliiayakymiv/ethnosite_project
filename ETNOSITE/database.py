import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            text TEXT NOT NULL,
            photo TEXT,
            date TEXT NOT NULL,
            timestamp INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_news(title, name, category, region, text, photo=None):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    timestamp = int(datetime.now().timestamp())
    
    c.execute('''
        INSERT INTO news (title, name, category, region, text, photo, date, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, name, category, region, text, photo, date, timestamp))
    
    conn.commit()
    conn.close()

def get_all_news():
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row  # доступ до полів через імена: n.title, n.name тощо
    c = conn.cursor()
    news = c.execute('SELECT * FROM news ORDER BY timestamp DESC').fetchall()
    conn.close()
    return news

def get_news_by_region(region):
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    news = c.execute(
        'SELECT * FROM news WHERE region=? ORDER BY timestamp DESC', (region,)
    ).fetchall()
    conn.close()
    return news