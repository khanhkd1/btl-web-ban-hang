from libraries.connect_database import connect_database, Address
from flask_restful import Resource
from flask import request, jsonify, make_response
from libraries.libraries import get_addresses
from sqlalchemy import exc

session = connect_database()


class AddressUserId(Resource):
	def get(self, user_id):
		session_tmp = session()
		try:
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": get_addresses(session_tmp, Address, user_id)
					}
				), 200
			)
		except exc as e:
			session_tmp.rollback()
			return make_response(
				jsonify(
					{
						"message": f"{e}",
						"data": {}
					}
				), 500
			)
		finally:
			session_tmp.close()

	def post(self, user_id):
		data = request.get_json()
		session_tmp = session()

		address = Address(
			user_id=user_id,
			full_name=data['full_name'],
			phone=data['phone'],
			address=data['address']
		)
		session_tmp.add(address)
		try:
			session_tmp.commit()
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": get_addresses(session_tmp, Address, user_id)
					}
				), 200
			)
		except exc as e:
			session_tmp.rollback()
			return make_response(
				jsonify(
					{
						"message": f"{e}",
						"data": {}
					}
				), 500
			)
		finally:
			session_tmp.close()


class AddressAddressId(Resource):
	def put(self, user_id, address_id):
		session_tmp = session()
		data = request.get_json()
		try:
			session_tmp.query(Address).filter_by(id=address_id).update(data)
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": get_addresses(session_tmp, Address, user_id)
					}
				), 200
			)
		except exc as e:
			session_tmp.rollback()
			return make_response(
				jsonify(
					{
						"message": f"{e}",
						"data": []
					}
				), 500
			)
		finally:
			session_tmp.close()

	def delete(self, user_id, address_id):
		session_tmp = session()
		session_tmp.query(Address).filter_by(id=address_id).delete()
		try:
			session_tmp.commit()
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": get_addresses(session_tmp, Address, user_id)
					}
				), 200
			)
		except exc as e:
			session_tmp.rollback()
			return make_response(
				jsonify(
					{
						"message": f"{e}",
						"data": []
					}
				), 500
			)
		finally:
			session_tmp.close()
