from flask import Flask
from flask_restful import Api
from modules.product.product_api import Home, ProductWithBrandId, Camera, Laptop, ProductWithProductId
from modules.cart_and_payment.cart_and_payments_api import CartWithUserId, BankWithUserId, BankWithoutUserId, PaymentAPI
from modules.user.user import UserWithoutUserId, UserWithUserId
from modules.address.address import AddressUserId, AddressAddressId
from libraries.connect_database import connect_database, User, Product, Brand, Cart, Payment, Bank, BankOfUser
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
admin.add_view(ModelView(Cart, session()))
admin.add_view(ModelView(Payment, session()))
admin.add_view(ModelView(Bank, session()))
admin.add_view(ModelView(BankOfUser, session()))

api = Api(app)

# api trang home
api.add_resource(Home, '/home', methods=['GET'])
# api.add_resource(ProductWithBrandId, '/brand/<int:brand_id>', methods=['GET'])

# api trang laptop
api.add_resource(Camera, '/product/camera', methods=['GET'])

# api trang camera
api.add_resource(Laptop, '/product/laptop', methods=['GET'])

# api lấy thông tin sản phẩm theo product_id
api.add_resource(ProductWithProductId, '/product/<int:product_id>', methods=['GET'])

# bank apis
# api.add_resource(BankWithoutUserId, '/bank', methods=['GET'])
# api.add_resource(BankWithUserId, '/bank/<int:user_id>', methods=['GET'])

# cart apis
# api.add_resource(CartWithUserId, '/cart/<int:user_id>',
#                  methods=['GET', 'POST', 'PUT', 'DELETE'])

# payment apis
# api.add_resource(PaymentAPI, '/payment/<int:user_id>', methods=['GET', 'POST'])

# api đăng nhập
api.add_resource(UserWithoutUserId, '/user', methods=['POST'])

# api lấy thông tin user, chỉnh sửa thông tin user
api.add_resource(UserWithUserId, '/user/<int:user_id>', methods=['GET', 'PUT'])

# user address apis
# api.add_resource(AddressUserId, '/user/address/<int:user_id>', methods=['GET', 'POST'])
# api.add_resource(AddressAddressId, '/user/address/<int:user_id>/<int:address_id>', methods=['PUT', 'DELETE'])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
