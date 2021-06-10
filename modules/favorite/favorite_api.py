from libraries.connect_database import connect_database, Product, Favorite
from libraries.libraries import get_favorites
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc


session = connect_database()


class FavoriteUser(Resource):
	def __init__(self):
		self.session = session()

	def get(self, user_id):
		favorites = get_favorites(self.session, Favorite, Product, user_id)
		self.session.close()
		return favorites


class FavoriteUserProduct(Resource):
	def __init__(self):
		self.session = session()

	def post(self, user_id, product_id):
		favorite = self.session.query(Favorite).filter_by(user_id=user_id, product_id=product_id).first()
		if favorite:
			return
		self.session.add(Favorite(user_id=user_id, product_id=product_id))
		self.session.commit()
		self.session.close()
		return

	def delete(self, user_id, product_id):
		self.session.query(Favorite).filter_by(user_id=user_id, product_id=product_id).delete()
		self.session.commit()
		self.session.close()
		return