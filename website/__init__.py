from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, LOGIN_MESSAGE

app = Flask(__name__)
app.config['SECRET_KEY']='kokdqwoiwenosjadoqwe oijqw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userapp:glowing123@localhost:5432/dbsf'
db = SQLAlchemy(app)
    
from .views import views
from .auth import auth
from .masters.mcolor import mcolor
from .masters.muom import muom
from .masters.mcategory import mcategory
from .masters.mitem import mitem

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

app.register_blueprint(mcolor,url_prefix='/mcolor')
app.register_blueprint(muom,url_prefix='/muom')
app.register_blueprint(mcategory,url_prefix='/mcategory')
app.register_blueprint(mitem,url_prefix='/mitem')
       
from .models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    