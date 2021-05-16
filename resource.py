from flask import Flask
from flask_restful import Api
from modules.test.Test import Test
from modules.camera.camera import CameraWithoutId
from libraries.connect_database import connect_database, Camera
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

session = connect_database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'khanhkd'
admin = Admin(app)
admin.add_view(ModelView(Camera, session()))
api = Api(app)

# Resource dashboard
api.add_resource(Test, '/', methods=['GET'])

api.add_resource(CameraWithoutId, '/camera', methods=['GET'])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as exp:
        print(exp)
