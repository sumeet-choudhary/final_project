from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from application.celery_config.make_celery import make_celery
load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "sumeet"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"
app.config["MONGO_URI"] = "mongodb://mongodb:27017/Users"

jwt = JWTManager(app)
mongo = PyMongo(app)

celery = make_celery(app)
