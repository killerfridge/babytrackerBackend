from .database import Base
from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from .utils import pwd_context


class Baby(Base):
    __tablename__ = 'babies'

    id = Column(Integer, primary_key=True, nullable=False)
    sleeps = relationship("Sleep", back_populates='baby')
    feeds = relationship("Feed", back_populates='baby')
    is_awake = Column(Boolean, nullable=False, server_default="True")
    is_feeding = Column(Boolean, nullable=False, server_default="False")
    sleep_sessions = relationship("SleepSession", back_populates="baby")


class Sleep(Base):
    __tablename__ = 'sleeps'

    id = Column(Integer, primary_key=True, nullable=False)
    sleep_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    is_awake = Column(Boolean, nullable=False)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete="CASCADE"), nullable=False)
    baby = relationship("Baby", back_populates="sleeps")


class SleepSession(Base):
    __tablename__ = 'sleepsession'

    id = Column(Integer, primary_key=True, nullable=False)
    sleep_start = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    sleep_end = Column(TIMESTAMP(timezone=True), nullable=True)
    sleep_length = Column(Float, nullable=True)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete="CASCADE"))
    baby = relationship("Baby", back_populates="sleep_sessions")

    def set_sleep_length(self):
        self.sleep_length = self.sleep_end - self.sleep_start

    def set_sleep_end(self):
        self.sleep_end = datetime.utcnow()


class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True, nullable=False)
    feed_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    is_start = Column(Boolean, nullable=False)
    baby_id = Column(Integer, ForeignKey("babies.id", ondelete="CASCADE"), nullable=False)
    baby = relationship("Baby", back_populates='feeds')
