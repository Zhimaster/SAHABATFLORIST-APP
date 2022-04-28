from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import true
from wtforms import Form, StringField, validators
from website import db
from website.utils import load_menu
from website.models import Category

mcategory = Blueprint('mcategory', __name__)

# Master Category Form Class
class MasterCategoryForm(Form):
    categoryid = StringField(None, 'Category ID')
    categorycode = StringField(None,'Category Code', [
        validators.DataRequired(),
        validators.Regexp('^[A-Z]+$',0,'First Name only allow Alphabet characters.'),
        validators.Length(min=1, max=20)])
    categoryname = StringField(None,'Category Name', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'Last Name only allow Alphabet characters.'),
        validators.Length(min=1, max=30),])
    
@mcategory.route('/')
@login_required
def index():
    menus = load_menu(current_user.user_group)
    form = MasterCategoryForm(request.form)
    all_data = Category.query.filter_by(active_flag=True).order_by(Category.category_id).all()
    return render_template('masters/mcategory.html', user=current_user, menus=menus, mcategories=all_data, form=form)

@mcategory.route('/insert', methods = ['POST'])
@login_required
def insert():
    if request.method == 'POST':
        category_code = request.form['categorycode']
        category_name = request.form['categoryname']
        
        getCategory = Category.query.filter(Category.category_code==category_code, Category.category_name==category_name).first()
        if getCategory:
            getCategory.active_flag = True
            db.session.commit()
        else:
            my_data = Category(category_code=category_code,category_name=category_name)
            db.session.add(my_data)
            db.session.commit()

        flash('Category : "'+category_name+'" has been added !', 'success')
        return redirect(url_for('mcategory.index'))
  
@mcategory.route('/update/<string:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        my_data = Category.query.get(id)
  
        my_data.category_code = request.form.get('categorycode'+id)
        my_data.category_name = request.form.get('categoryname'+id)
          
        db.session.commit()
        flash('Category : "'+my_data.category_name+'" has been updated !', 'success')
        return redirect(url_for('mcategory.index'))
  
@mcategory.route('/delete/<string:id>', methods = ['GET', 'POST'])
@login_required
def delete(id):
    if request.method == 'POST':
        my_data = Category.query.get(id)
        my_data.active_flag = False
          
        db.session.commit()
        flash('Category : "'+my_data.category_name+'" has been deleted !', 'success')
        return redirect(url_for('mcategory.index'))