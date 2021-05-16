from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float


Base = declarative_base()


def connect_database():
    engine = create_engine('mysql://root:vjpvjp123A01@47.254.253.64/lap_trinh_web_api?charset=utf8mb4')
    session = sessionmaker(bind=engine)
    return session


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    resolution = Column(String, nullable=False)
    location = Column(String, nullable=False)
    images = Column(String)
    type = Column(String, nullable=False)
    visibility = Column(String, nullable=False)
    power = Column(String)
    other = Column(String)
