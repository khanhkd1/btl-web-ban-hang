from libraries.connect_database import connect_database, Product, Cart, Bank, BankOfUser, User, Payment
from libraries.libraries import get_carts, get_banks_of_user, get_banks, get_payments, get_payment_types, get_all_payments
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc
import datetime

session = connect_database()


class PaymentTypeAPI(Resource):
	def __init__(self):
		self.session = session()

	def get(self):
		payment_types = get_payment_types(self.session)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": payment_types
				}
			), 200
		)


class AdminPaymentAll(Resource):
	def __init__(self):
		self.session = session()

	def get(self):
		payments = get_all_payments(self.session)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"payments": payments
				}
			), 200
		)


class AdminPayment(Resource):
	def __init__(self):
		self.session = session()

	def put(self, payment_id):
		data = request.get_json()
		self.session.query(Payment).filter_by(id=payment_id).update(
			{
				"status": data['status'],
				'admin_confirm': True,
				"updated_at": str(datetime.datetime.now())
			}
		)
		self.session.commit()
		payments = get_all_payments(self.session)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"payments": payments
				}
			), 200
		)


class PaymentAPI(Resource):
	def __init__(self):
		self.session = session()

	def get(self, user_id):
		payments = get_payments(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": payments
				}
			), 200
		)

	def post(self, user_id):
		data = request.get_json()
		carts = get_carts(self.session, user_id)
		products = '-'.join([str([x['product_id'], x['amount'], x['total_price']]) for x in carts])

		payment = Payment(
			user_id=user_id,
			address_id=data['address_id'],
			payment_type_id=data['payment_type_id'],
			products=products,
			total=sum([x['total_price'] for x in carts]),
			created_at=str(datetime.datetime.now()),
			updated_at=str(datetime.datetime.now()),
			admin_confirm=False,
			status='Chờ xác nhận'
		)
		self.session.add(payment)
		self.session.commit()
		for cart in carts:
			self.session.query(Cart).filter_by(id=cart['id']).delete()
			self.session.commit()
			self.session.query(Product).filter_by(id=cart['product_id']).update({
					'quantity': self.session.query(Product).filter_by(id=cart['product_id']).first().quantity - cart['amount']
				})
			self.session.commit()
		payments = get_payments(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": payments
				}
			), 200
		)

	def delete(self, user_id):
		data = request.get_json()
		payment = self.session.query(Payment).filter_by(id=data['payment_id']).first()
		if not payment.admin_confirm:
			self.session.query(Payment).filter_by(id=data['payment_id']).delete()
			self.session.commit()
		payments = get_payments(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": payments
				}
			), 200
		)
