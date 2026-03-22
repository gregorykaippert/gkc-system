# from flask import Flask, render_template, url_for, request, redirect, flash
from flask import Flask
from gkcsystems.secret_key import secret_key
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key

if os.getenv("DATABASE_URL"): # verifica se existe variavel ambiente, no caso em producao
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else: # se tiver localhost, usa o banco local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gkcsystemdb.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = r'postgresql://postgres:GMorWkOZyYavMhehxOpvwrHxOYxTPXSq@centerbeam.proxy.rlwy.net:19962/railway'

database = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from gkcsystems import routes