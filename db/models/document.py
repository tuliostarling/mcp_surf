from sqlalchemy import Column, Integer, String
from db.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    content = Column(String)
