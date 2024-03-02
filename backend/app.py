from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os 
from dotenv import load_dotenv
load_dotenv()
from route import *

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# # Configuring the mongo database
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 


mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')

# MONGO_HOST = 'localhost'  # for Local MongoDB connection
MONGO_HOST = 'mongodb-svc'
MONGO_PORT = 27017
MONGO_DB = 'quiz_database'

mongo_client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{MONGO_HOST}:{MONGO_PORT}/')
mongo_db = mongo_client[MONGO_DB]
users_collection = mongo_db['users']
questions_collection = mongo_db['questions']
scores_collection = mongo_db['scores']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)