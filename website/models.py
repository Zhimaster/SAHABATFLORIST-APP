from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Menu(db.Model):
    __tablename__ = 'tbusergroup_menu'
    user_group = db.Column(db.String(20), nullable=False, primary_key=True)
    menu_code = db.Column(db.String(20), nullable=False, primary_key=True)
    menu_caption = db.Column(db.String(30), nullable=False, default='Not Set')
    menu_order = db.Column(db.SMALLINT)
    parent_menu = db.Column(db.String(20))
    active_flag = db.Column(db.Boolean, nullable=False, default=True)
    
                     
class Status(db.Model):
    __tablename__ = 'tbstatus'
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(20), nullable=False)
    users = db.relationship('User')


class User(db.Model, UserMixin):
    __tablename__ = 'tbuser'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_group = db.Column(db.String(35), nullable=False)  
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('tbstatus.status_id'), nullable=False, default=0)
     

class Color(db.Model):
    __tablename__ = 'tbcolor'
    color_id = db.Column(db.Integer, primary_key=True)
    color_code = db.Column(db.String(20), unique=True, nullable=False)
    color_name = db.Column(db.String(30), unique=True, nullable=False)
    active_flag = db.Column(db.Boolean, nullable=False, default=True)
    items = db.relationship('Item')


class Uom(db.Model):
    __tablename__ = 'tbuom'
    uom_code = db.Column(db.String(10), primary_key=True)
    uom_name = db.Column(db.String(20), unique=True, nullable=False)
    active_flag = db.Column(db.Boolean, nullable=False, default=True)
    items = db.relationship('Item')
    
    
class Category(db.Model):
    __tablename__ = 'tbcategory'
    category_id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(20), unique=True, nullable=False)
    category_name = db.Column(db.String(30), unique=True, nullable=False)
    active_flag = db.Column(db.Boolean, nullable=False, default=True)
    items = db.relationship('Item')


class Item(db.Model):
    __tablename__ = 'tbitem'
    item_id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(50), unique=True, nullable=False, comment='consist of 1 digit Area, 3 digit category_id, 6 digit item_id, 3 digit color_id')
    item_name = db.Column(db.String(50), unique=True, nullable=False)
    item_type = db.Column(db.String(30), nullable=False)
    barcode_str = db.Column(db.String(20), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('tbcategory.category_id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('tbcolor.color_id'))
    uom_code = db.Column(db.String(10), db.ForeignKey('tbuom.uom_code'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('tbstatus.status_id'), nullable=False, default=0)
    active_flag = db.Column(db.Boolean, nullable=False, default=True)