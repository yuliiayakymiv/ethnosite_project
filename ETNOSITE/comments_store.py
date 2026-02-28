import json
from datetime import datetime
from pathlib import Path

# Коментарі зберігаємо у файлі instance/comments.json
COMMENTS_FILE = Path('instance/comments.json')

def _load_all():
    """Завантажує всі коментарі (dict: news_id -> list[comment])."""
    if not COMMENTS_FILE.exists():
        return {}
    try:
        with COMMENTS_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_all(data: dict):
    """Зберігає всі коментарі у файл."""
    COMMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with COMMENTS_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_comments(news_id: int):
    """Повертає список коментарів конкретної новини."""
    data = _load_all()
    return data.get(str(news_id), [])

def add_comment(news_id: int, name: str, text: str):
    """Додає новий коментар і зберігає зміни у файл."""
    data = _load_all()
    items = data.get(str(news_id), [])
    items.insert(0, {
        "name": name.strip(),
        "text": text.strip(),
        "created_at": datetime.now().strftime('%d.%m.%Y %H:%M')
    })
    data[str(news_id)] = items
    _save_all(data)
