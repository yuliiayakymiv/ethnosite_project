from sqlalchemy import Column, Integer, String, Text
from database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    region = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    photo = Column(String)
    date = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)