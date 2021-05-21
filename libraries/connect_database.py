from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


def connect_database():
    engine = create_engine('mysql://root:vjpvjp123A01@47.254.253.64/lap_trinh_web_api?charset=utf8mb4')
    session = sessionmaker(bind=engine)
    return session


class CameraBrand(Base):
    __tablename__ = 'camera_brand'
    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False, unique=True)
    brands = relationship('Camera', backref='camera_brand')

    def __repr__(self):
        return self.brand


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, primary_key=True)
    brand = Column(Integer, ForeignKey('camera_brand.id'))
    productName = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    images = Column(String)
    productSummary = Column(String, nullable=False)
    warranty = Column(String, nullable=False)


class LaptopBrand(Base):
    __tablename__ = 'laptop_brand'
    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False, unique=True)
    brands = relationship('Laptop', backref='laptop_brand')

    def __repr__(self):
        return self.brand


class Laptop(Base):
    __tablename__ = 'laptop'
    id = Column(Integer, primary_key=True)
    brand = Column(Integer, ForeignKey('laptop_brand.id'))
    productName = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    images = Column(String)
    productSummary = Column(String, nullable=False)
    warranty = Column(String, nullable=False)


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
