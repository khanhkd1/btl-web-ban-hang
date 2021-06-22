from libraries.connect_database import connect_database, Address
from flask_restful import Resource
from flask import request, jsonify, make_response
from libraries.libraries import get_addresses

session = connect_database()


class AddressUserAPI(Resource):
	def __init__(self):
		self.session = session()

	def get(self, user_id):
		addresses = get_addresses(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": addresses,
					"note": "1 user có thể có nhiều địa chỉ nhận hàng khác nhau với người nhận khác nhau"
				}
			), 200
		)

	def post(self, user_id):
		data = request.get_json()
		self.session.add(Address(
				user_id=user_id,
				full_name=data['full_name'],
				phone=data['phone'],
				address=data['address']
			))
		self.session.commit()
		addresses = get_addresses(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": addresses,
					"note": "1 user có thể có nhiều địa chỉ nhận hàng khác nhau với người nhận khác nhau"
				}
			), 200
		)

	def put(self, user_id):
		data = request.get_json()
		address_id = data['address_id']
		del data['address_id']
		self.session.query(Address).filter_by(id=address_id).update(data)
		self.session.commit()
		addresses = get_addresses(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": addresses,
					"note": "1 user có thể có nhiều địa chỉ nhận hàng khác nhau với người nhận khác nhau"
				}
			), 200
		)

	def delete(self, user_id):
		data = request.get_json()
		self.session.query(Address).filter_by(id=data['address_id']).delete()
		self.session.commit()
		addresses = get_addresses(self.session, user_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": addresses,
					"note": "1 user có thể có nhiều địa chỉ nhận hàng khác nhau với người nhận khác nhau"
				}
			), 200
		)
