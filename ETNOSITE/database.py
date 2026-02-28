import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель новини (база для вашого застосунку)
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    name = Column(String(100))
    category = Column(String(100))
    region = Column(String(100))
    text = Column(Text)
    photo = Column(String(255))
    date = Column(String(50))
    timestamp = Column(Integer)
    # Поля для реакцій (якщо ви їх використовуєте)
    hug_count = Column(Integer, default=0)
    fire_count = Column(Integer, default=0)
    up_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    love_count = Column(Integer, default=0)

# Функції для роботи з БД
def add_news(title, name, category, region, text, photo=None):
    db = SessionLocal()
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    timestamp = int(datetime.now().timestamp())
    news_item = News(
        title=title, name=name, category=category,
        region=region, text=text, photo=photo,
        date=date, timestamp=timestamp
    )
    db.add(news_item)
    db.commit()
    db.close()

def get_all_news():
    db = SessionLocal()
    news = db.query(News).order_by(News.timestamp.desc()).all()
    db.close()
    return news

def get_news_by_region(region):
    db = SessionLocal()
    news = db.query(News).filter(News.region == region).order_by(News.timestamp.desc()).all()
    db.close()
    return news

# Ініціалізація таблиць
def init_db():
    Base.metadata.create_all(bind=engine)
