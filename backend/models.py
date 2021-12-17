from .database import Base
from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Float, Interval, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime, timezone
from .utils import pwd_context
import enum


class Nappy(enum.Enum):
    wee = 1
    poo = 2
    wee_poo = 3


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    baby = relationship("Baby", back_populates="user")

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class Baby(Base):
    __tablename__ = 'babies'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    sleeps = relationship("Sleep", back_populates='baby')
    feeds = relationship("Feed", back_populates='baby')
    is_awake = Column(Boolean, nullable=False, server_default="True")
    is_feeding = Column(Boolean, nullable=False, server_default="False")
    sleep_sessions = relationship("SleepSession", back_populates="baby")
    feed_sessions = relationship("FeedSession", back_populates="baby")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="baby")
    weights = relationship("Weight", back_populates="baby")
    temperatures = relationship("Temperature", back_populates="baby")
    nappy_changes = relationship("NappyChanges", back_populates='baby')


class Sleep(Base):
    __tablename__ = 'sleeps'

    id = Column(Integer, primary_key=True, nullable=False)
    sleep_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    is_awake = Column(Boolean, nullable=False)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="sleeps")


class SleepSession(Base):
    __tablename__ = 'sleepsessions'

    id = Column(Integer, primary_key=True, nullable=False)
    sleep_start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    sleep_end = Column(TIMESTAMP(timezone=True), nullable=True)
    sleep_length = Column(Interval, nullable=True)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="sleep_sessions")

    def set_sleep_end(self):
        self.sleep_end = datetime.now(timezone.utc)

    def set_sleep_length(self):
        self.set_sleep_end()
        self.sleep_length = self.sleep_end - self.sleep_start


class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True, nullable=False)
    feed_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    is_start = Column(Boolean, nullable=False)
    baby_id = Column(Integer, ForeignKey("babies.id", ondelete="CASCADE"))
    baby = relationship("Baby", back_populates='feeds')


class FeedSession(Base):
    __tablename__ = 'feedsessions'

    id = Column(Integer, primary_key=True, nullable=False)
    feed_start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    feed_end = Column(TIMESTAMP(timezone=True), nullable=True)
    feed_length = Column(Interval, nullable=True)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="feed_sessions")

    def set_feed_end(self):
        self.feed_end = datetime.now(timezone.utc)

    def set_feed_length(self):
        self.set_feed_end()
        self.feed_length = self.feed_end - self.feed_start


class Weight(Base):
    __tablename__ = 'weights'

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    baby_id = Column(Integer, ForeignKey("babies.id", ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="weights")


class Temperature(Base):
    __tablename__ = 'temperatures'

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    baby_id = Column(Integer, ForeignKey("babies.id", ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="temperatures")


class NappyChanges(Base):
    __tablename__ = 'nappies'

    id = Column(Integer, primary_key=True, nullable=False)
    nappy_type = Column(Enum(Nappy))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    baby_id = Column(Integer, ForeignKey("babies.id", ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="nappy_changes")
