from flask import Flask
from flask_restful import Api
from modules.camera.camera import CameraWithoutId
from modules.laptop.laptop import LaptopWithoutId
from modules.user.user import UserApi
from libraries.connect_database import connect_database, Camera, User, Laptop
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

session = connect_database()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'khanhkd'

admin = Admin(app)
admin.add_view(ModelView(Camera, session()))
admin.add_view(ModelView(Laptop, session()))
admin.add_view(ModelView(User, session()))

api = Api(app)
api.add_resource(CameraWithoutId, '/camera', methods=['GET'])
api.add_resource(LaptopWithoutId, '/laptop', methods=['GET'])
api.add_resource(UserApi, '/user', methods=['POST'])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
