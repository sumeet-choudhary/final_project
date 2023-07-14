from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "sumeet"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"

jwt = JWTManager(app)
mongo = PyMongo(app)
