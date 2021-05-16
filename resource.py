from flask import Flask
from flask_restful import Api
from modules.test.Test import Test
from modules.camera.camera import CameraWithoutId


app = Flask(__name__)
api = Api(app)

# Resource dashboard
api.add_resource(Test, '/', methods=['GET'])

api.add_resource(CameraWithoutId, '/camera', methods=['GET'])

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as exp:
        print(exp)
