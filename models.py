from sqlalchemy import Column, Integer
from database import Base


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, nullable=True)
    tg_chat_id = Column(Integer, nullable=False, unique=True)
