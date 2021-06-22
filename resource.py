from flask import Flask
from flask_restful import Api
from libraries.connect_database import connect_database, User, Product, Brand, Cart, Payment, Bank, BankOfUser
from flask_cors import CORS
from modules.product.product_api import Home, ProductWithBrandId, Camera, Laptop, ProductWithProductId
from modules.user.user_api import UserAPI, SignIn, SignUp
from modules.favorite.favorite_api import FavoriteUser, FavoriteUserProduct
from modules.cart.cart_api import CartUser, CartUserProduct
from modules.bank.bank_api import BankAPI, BankUserAPI
from modules.address.address_api import AddressUserAPI
from modules.payment.payment_api import PaymentAPI, PaymentTypeAPI


session = connect_database()

app = Flask(__name__)

cors = CORS(app)

app.config['SECRET_KEY'] = 'khanhkd'

api = Api(app)

# api trang home
api.add_resource(Home, '/home', methods=['GET'])

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

# api quản lý danh sách yêu thích
api.add_resource(FavoriteUserProduct, '/user/favorite/<int:user_id>/<int:product_id>', methods=['POST', 'DELETE'])

# api lấy danh sách giỏ hàng
api.add_resource(CartUser, '/user/cart/<int:user_id>', methods=['GET'])

# api quản lý giỏ hàng
api.add_resource(CartUserProduct, '/user/cart/<int:user_id>/<int:product_id>', methods=['POST', 'PUT', 'DELETE'])

# api quản lý thông tin người dùng
api.add_resource(UserAPI, '/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])

# api lấy danh sách ngân hàng được phép liên kết
api.add_resource(BankAPI, '/bank', methods=['GET'])

# api quản lý thông tin ngân hàng liên kết của user
api.add_resource(BankUserAPI, '/user/bank/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])

# api quản lý thông tin địa chỉ của user
api.add_resource(AddressUserAPI, '/user/address/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])

# api lấy danh sách các loại thanh toán
api.add_resource(PaymentTypeAPI, '/paymenttype', methods=['GET'])

# api quản lý thanh toán
api.add_resource(PaymentAPI, '/payment/<int:user_id>', methods=['GET', 'POST', 'DELETE'])


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
