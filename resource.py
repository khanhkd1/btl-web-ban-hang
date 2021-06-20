from flask import Flask
from flask_restful import Api
from libraries.connect_database import connect_database, User, Product, Brand, Cart, Payment, Bank, BankOfUser
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

from modules.product.product_api import Home, ProductWithBrandId, Camera, Laptop, ProductWithProductId
from modules.user.user_api import UserAPI, SignIn, SignUp
from modules.favorite.favorite_api import FavoriteUser, FavoriteUserProduct
from modules.cart.cart_api import CartUser, CartUserProduct
from modules.bank.bank_api import BankAPI, BankUserAPI, BankUserBankAPI
# from modules.address.address import AddressUserId, AddressAddressId


session = connect_database()

app = Flask(__name__)

cors = CORS(app)

app.config['SECRET_KEY'] = 'khanhkd'

# admin = Admin(app)

# admin.add_view(ModelView(User, session()))
# admin.add_view(ModelView(Product, session()))
# admin.add_view(ModelView(Brand, session()))
# admin.add_view(ModelView(Cart, session()))
# admin.add_view(ModelView(Payment, session()))
# admin.add_view(ModelView(Bank, session()))
# admin.add_view(ModelView(BankOfUser, session()))

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

# api đăng nhập
api.add_resource(SignIn, '/user/signin', methods=['POST'])

# api đăng ký
api.add_resource(SignUp, '/user/signup', methods=['POST'])

# api lấy danh sách yêu thích
api.add_resource(FavoriteUser, '/user/favorite/<int:user_id>', methods=['GET'])

# api thêm sản phẩm vào danh sách yêu thích, xoá sản phẩm khỏi danh sách yêu thích
api.add_resource(FavoriteUserProduct, '/user/favorite/<int:user_id>/<int:product_id>', methods=['POST', 'DELETE'])

# api lấy danh sách giỏ hàng
api.add_resource(CartUser, '/user/cart/<int:user_id>', methods=['GET'])

# api thêm sản phẩm vào danh sách giỏ hàng, sửa số lượng sản phẩm trong giỏ hàng, xoá sản phẩm khỏi giỏ hàng
api.add_resource(CartUserProduct, '/user/cart/<int:user_id>/<int:product_id>', methods=['POST', 'PUT', 'DELETE'])


# api lấy thông tin, chỉnh sửa thông tin, xoá user
api.add_resource(UserAPI, '/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])

# # api lấy danh sách ngân hàng được phép liên kết
# api.add_resource(BankAPI, '/bank', methods=['GET'])

# # api lấy danh sách ngân hàng đã liên kết với user
# api.add_resource(BankUserAPI, '/user/bank/<int:user_id>', methods=['GET'])

# # api thêm ngân hàng liên kết với user, sửa thông tin số tài khoản
# api.add_resource(BankUserBankAPI, '/user/bank/<int:user_id>/<int:bank_id>', methods=['POST', 'PUT', 'DELETE'])



# bank apis
# api.add_resource(BankWithoutUserId, '/bank', methods=['GET'])
# api.add_resource(BankWithUserId, '/bank/<int:user_id>', methods=['GET'])

# cart apis
# api.add_resource(CartWithUserId, '/cart/<int:user_id>',
#                  methods=['GET', 'POST', 'PUT', 'DELETE'])

# payment apis
# api.add_resource(PaymentAPI, '/payment/<int:user_id>', methods=['GET', 'POST'])

# user address apis
# api.add_resource(AddressUserId, '/user/address/<int:user_id>', methods=['GET', 'POST'])
# api.add_resource(AddressAddressId, '/user/address/<int:user_id>/<int:address_id>', methods=['PUT', 'DELETE'])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
