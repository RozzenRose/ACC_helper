from app.DB_settings.DB_engine import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Interval


class UsersOrm(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, unique=True)
    username = Column(String)
    user_language = Column(String)

class Tracks(Base):
    __tablename__ = 'Tracks'
    id = Column(Integer, primary_key=True, unique=True)
    track_name = Column(String)
    turns = Column(Integer)
    aproximate_flow = Column(Float)
    aproximate_time = Column(Interval)

### Написать модели для Cars и Info ###

class Cars(Base):
    __tablename__ = 'Cars'
    id = Column(Integer, primary_key=True, unique=True)
    car_name = Column(String, nullable=False)

class Info(Base):
    __tablename__ = 'Info'
    id = Column(Integer, primary_key=True, unique=True)
    car_id = Column(Integer, ForeignKey('Cars.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('Tracks.id'), nullable=False)
    track_guide = Column(String)  # ссылка на YouTube или другой источник
    setups = Column(String)  # можно "+" или путь к файлу/описанию