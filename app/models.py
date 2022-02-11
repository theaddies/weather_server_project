from decimal import Decimal
from sqlalchemy import Column, Integer, Float, String, SmallInteger, DateTime, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key = True, nullable = False)
    temp = Column(SmallInteger, nullable = False, default = 0)
    press = Column(SmallInteger, nullable = False, default = 0)
    humid = Column(SmallInteger, nullable = False, default = 0)
    wind_speed = Column(SmallInteger, nullable = False, default = 0)
    wind_direction = Column(SmallInteger, nullable = False, default = 0)
    event_direction = Column(SmallInteger, nullable = False, default = 0)
    bno_direction = Column(SmallInteger, nullable = False, default = 0)
    current = Column(SmallInteger, nullable = False, default = 0)
    voltage = Column(Float, nullable = False, default = 0)
    power = Column(SmallInteger, nullable = False, default = 0.)
    #date = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

    # owner_id = Column(Integer, ForeignKey(
    #     "users.id", ondelete="CASCADE"), nullable=False)

    # owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "weather_data.id", ondelete="CASCADE"), primary_key=True)