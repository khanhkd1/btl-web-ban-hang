from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


def connect_database():
	engine = create_engine('mysql://root:vjpvjp123A01@47.254.253.64/lap_trinh_web_api?charset=utf8mb4')
	session = sessionmaker(bind=engine)
	return session


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
	password = Column(String(255), nullable=False)
	is_admin = Column(Boolean)

	product = relationship('Product', secondary='cart')

	def __init__(self, username, password, is_admin):
		self.username = username
		self.set_password(password)
		self.is_admin = is_admin

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)


class Brand(Base):
	__tablename__ = 'brand'
	id = Column(Integer, primary_key=True)
	brand = Column(String, nullable=False)
	is_laptop = Column(Boolean)
	is_camera = Column(Boolean)

	product_brand = relationship('Product', backref='brand')

	def __repr__(self):
		return self.brand


class Product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True)
	brand_id = Column(Integer, ForeignKey('brand.id'))
	productName = Column(String, nullable=False)
	quantity = Column(Integer, nullable=False)
	price = Column(Float, nullable=False)
	images = Column(String)
	productSummary = Column(String, nullable=False)
	warranty = Column(String, nullable=False)

	user = relationship('User', secondary='cart')

	def __repr__(self):
		return self.productName


class Cart(Base):
	__tablename__ = 'cart'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
	amount = Column(Integer)

