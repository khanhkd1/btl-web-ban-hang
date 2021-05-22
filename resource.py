from flask import Flask
from flask_restful import Api
from modules.product.product_api import Home, ProductWithBrandId
from modules.cart_and_payment.cart_and_payments_api import CartWithUserId
from modules.user.user import UserWithoutUserId, UserWithUserId
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

# cart apis
api.add_resource(CartWithUserId, '/cart/<int:user_id>')

# user apis
api.add_resource(UserWithoutUserId, '/user', methods=['POST'])
api.add_resource(UserWithUserId, '/user/<int:user_id>', methods=['PUT'])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
