from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String, unique=True, index=True)
    url = Column(String)
    alias = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

