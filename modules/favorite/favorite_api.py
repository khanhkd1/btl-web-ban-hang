from libraries.connect_database import connect_database, Favorite
from libraries.libraries import get_favorites
from flask_restful import Resource


session = connect_database()


class FavoriteUser(Resource):
	def __init__(self):
		self.session = session()

	def get(self, user_id):
		favorites = get_favorites(self.session, user_id)
		self.session.close()
		return favorites


class FavoriteUserProduct(Resource):
	def __init__(self):
		self.session = session()

	def post(self, user_id, product_id):
		favorite = self.session.query(Favorite).filter_by(user_id=user_id, product_id=product_id).first()
		if not favorite:
			self.session.add(Favorite(user_id=user_id, product_id=product_id))
			self.session.commit()
		favorites = get_favorites(self.session, user_id)
		self.session.close()
		return favorites

	def delete(self, user_id, product_id):
		self.session.query(Favorite).filter_by(user_id=user_id, product_id=product_id).delete()
		self.session.commit()
		favorites = get_favorites(self.session, user_id)
		self.session.close()
		return favorites
