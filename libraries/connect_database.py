from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean)

    def __init__(self, username, password, is_admin):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
