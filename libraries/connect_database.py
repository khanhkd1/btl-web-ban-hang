from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Date
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


def connect_database():
	engine = create_engine('mysql://khanhkd:pass@localhost/btl-web-ban-hang?charset=utf8mb4', pool_size=10, max_overflow=20)
	session = sessionmaker(bind=engine)
	return session


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, nullable=False)
	password = Column(String(255), nullable=False)
	is_admin = Column(Boolean, nullable=False)
	full_name = Column(String)
	phone = Column(String(10))
	email = Column(String)
	gender = Column(String)
	date_of_birth = Column(String)

	product = relationship('Product', secondary='cart')
	bank = relationship('Bank', secondary='bank_of_user', back_populates='user')

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)
		self.is_admin = False
		self.full_name = ''
		self.phone = ''
		self.email = ''
		self.gender = 'Nam'
		self.date_of_birth = '01/01/1970'

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)


class Address(Base):
	__tablename__ = 'address'
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	full_name = Column(String)
	phone = Column(String)
	address = Column(String)


class Brand(Base):
	__tablename__ = 'brand'
	id = Column(Integer, primary_key=True, autoincrement=True)
	brand = Column(String, nullable=False)
	is_laptop = Column(Boolean)
	is_camera = Column(Boolean)


class Product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True, autoincrement=True)
	brand_id = Column(Integer, ForeignKey('brand.id'), primary_key=True)
	productName = Column(String, nullable=False)
	quantity = Column(Integer, nullable=False)
	price = Column(Float, nullable=False)
	images = Column(String)
	productSummary = Column(String, nullable=False)
	warranty = Column(String, nullable=False)

	brand = relationship('Brand', backref='product')
	user = relationship('User', secondary='cart', back_populates='product')


class Cart(Base):
	__tablename__ = 'cart'
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
	amount = Column(Integer)
	total_price = Column(Float)


class Favorite(Base):
	__tablename__ = 'favorite'
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)


class Bank(Base):
	__tablename__ = 'bank'
	id = Column(Integer, primary_key=True, autoincrement=True)
	bank_name = Column(String)

	user = relationship('User', secondary='bank_of_user', back_populates='bank')


class BankOfUser(Base):
	__tablename__ = 'bank_of_user'
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	bank_id = Column(Integer, ForeignKey('bank.id'), primary_key=True)
	bank_number = Column(String)


class PaymentType(Base):
	__tablename__ = 'payment_type'
	id = Column(Integer, primary_key=True)
	name = Column(String)


class Payment(Base):
	__tablename__ = 'payment'
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	address_id = Column(Integer, ForeignKey('address.id'), primary_key=True)
	payment_type_id = Column(Integer, ForeignKey('payment_type.id'), primary_key=True)
	products = Column(String)
	total = Column(Float)
	created_at = Column(String)
	updated_at = Column(String)
	admin_confirm = Column(Boolean)
	status = Column(String)


class VisitsLog(Base):
	__tablename__ = 'visits_log'
	id = Column(Integer, primary_key=True)
	ip_address = Column(String)
	requested_url = Column(String)
	referer_page = Column(String)
	page_name = Column(String)
	query_string = Column(String)
	user_agent = Column(String)
	date = Column(String)
