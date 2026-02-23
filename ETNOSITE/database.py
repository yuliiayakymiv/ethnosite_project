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
            timestamp INTEGER NOT NULL,
            hug_count INTEGER DEFAULT 0,
            fire_count INTEGER DEFAULT 0,
            up_count INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            love_count INTEGER DEFAULT 0
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

def update_reaction(news_id, reaction_type, action='add'):
    reactions = {
        'hug': 'hug_count',
        'fire': 'fire_count',
        'up': 'up_count',
        'like': 'like_count',
        'love': 'love_count'
    }
    column = reactions.get(reaction_type)
    if not column: return None

    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    # Визначаємо операцію: +1 або -1
    change = 1 if action == 'add' else -1

    # Оновлюємо, але не дозволяємо лічильнику стати менше 0
    c.execute(f'''UPDATE news
                  SET {column} = MAX(0, {column} + ?)
                  WHERE id = ?''', (change, news_id))

    res = c.execute('''SELECT hug_count, fire_count, up_count, like_count, love_count
                       FROM news WHERE id = ?''', (news_id,)).fetchone()
    conn.commit()
    conn.close()

    return {
        "hug": res[0], "fire": res[1], "up": res[2],
        "like": res[3], "love": res[4]
    }
