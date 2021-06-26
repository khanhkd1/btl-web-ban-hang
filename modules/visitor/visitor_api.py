from libraries.connect_database import connect_database
from flask_restful import Resource
from libraries.libraries import get_visitors

session = connect_database()


class VisitorAPI(Resource):
	def __init__(self):
		self.session = session()

	def get(self):
		visitors = get_visitors(self.session)
		self.session.close()
		return visitors
