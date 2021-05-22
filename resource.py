from flask import Flask
from flask_restful import Api
from modules.product.product_api import Home, ProductWithBrandId
from modules.user.user import UserApi
from libraries.connect_database import connect_database, User, Product, Brand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

session = connect_database()

app = Flask(__name__)

cors = CORS(app)

app.config['SECRET_KEY'] = 'khanhkd'

admin = Admin(app)

admin.add_view(ModelView(User, session()))
admin.add_view(ModelView(Product, session()))
admin.add_view(ModelView(Brand, session()))

api = Api(app)

# product apis
api.add_resource(Home, '/home', methods=['GET'])
api.add_resource(ProductWithBrandId, '/brand/<int:brand_id>', methods=['GET'])

api.add_resource(UserApi, '/user', methods=['POST'])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
