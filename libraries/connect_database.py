from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


def connect_database():
	engine = create_engine('mysql://root:vjpvjp123A01@47.254.253.64/lap_trinh_web_api?charset=utf8mb4', pool_size=20, max_overflow=0)
	session = sessionmaker(bind=engine)
	return session


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
	password = Column(String(255), nullable=False)
	is_admin = Column(Boolean, nullable=False)
	full_name = Column(String)
	phone = Column(String(10))
	email = Column(String)

	product = relationship('Product', secondary='cart')
	bank = relationship('Bank', secondary='bank_of_user')

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)
		self.is_admin = False
		self.full_name = ''
		self.phone = ''
		self.email = ''

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def __repr__(self):
		return self.username


class Address(Base):
	__tablename__ = 'address'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	full_name = Column(String)
	phone = Column(String)
	address = Column(String)


class Brand(Base):
	__tablename__ = 'brand'
	id = Column(Integer, primary_key=True)
	brand = Column(String, nullable=False)
	is_laptop = Column(Boolean)
	is_camera = Column(Boolean)

	def __repr__(self):
		return self.brand


class Product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True)
	brand_id = Column(Integer, ForeignKey('brand.id'), primary_key=True)
	productName = Column(String, nullable=False)
	quantity = Column(Integer, nullable=False)
	price = Column(Float, nullable=False)
	images = Column(String)
	productSummary = Column(String, nullable=False)
	warranty = Column(String, nullable=False)

	brand = relationship('Brand', backref='product')
	user = relationship('User', secondary='cart')

	def __repr__(self):
		return self.productName


class Cart(Base):
	__tablename__ = 'cart'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
	amount = Column(Integer)
	total_price = Column(Float)

	user = relationship('User', backref='cart')
	product = relationship('Product', backref='cart')

	def __repr__(self):
		return str(self.id)


class Favorite(Base):
	__tablename__ = 'favorite'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)


class Bank(Base):
	__tablename__ = 'bank'
	id = Column(Integer, primary_key=True)
	bank_name = Column(String)

	user = relationship('User', secondary='bank_of_user')

	def __repr__(self):
		return self.bank_name


class BankOfUser(Base):
	__tablename__ = 'bank_of_user'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	bank_id = Column(Integer, ForeignKey('bank.id'), primary_key=True)
	bank_number = Column(String)

	user = relationship('User', backref='bank_of_user')
	bank = relationship('Bank', backref='bank_of_user')

	def __repr__(self):
		return str(self.id)


class Payment(Base):
	__tablename__ = 'payment'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	products = Column(String)
	total = Column(Float)
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	cancel = Column(Boolean)
	admin_confirm = Column(Boolean)
	status = Column(String)

	user = relationship('User', backref='payment')

	def __repr__(self):
		return str(self.id)
