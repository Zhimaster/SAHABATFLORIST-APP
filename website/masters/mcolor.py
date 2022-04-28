from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import true
from wtforms import Form, StringField, validators
from website import db
from website.utils import load_menu
from website.models import Color

mcolor = Blueprint('mcolor', __name__)

# Master Color Form Class
class MasterColorForm(Form):
    colorid = StringField(None, 'Color ID')
    colorcode = StringField(None,'Color Code', [
        validators.DataRequired(),
        validators.Regexp('^[A-Z]+$',0,'First Name only allow Alphabet characters.'),
        validators.Length(min=1, max=20)])
    colorname = StringField(None,'Color Name', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'Last Name only allow Alphabet characters.'),
        validators.Length(min=1, max=30),])
    
@mcolor.route('/')
@login_required
def index():
    menus = load_menu(current_user.user_group)
    form = MasterColorForm(request.form)
    all_data = Color.query.filter_by(active_flag=True).order_by(Color.color_id).all()
    return render_template('masters/mcolor.html', user=current_user, menus=menus, mcolors=all_data, form=form)

@mcolor.route('/insert', methods = ['POST'])
@login_required
def insert():
    if request.method == 'POST':
        color_code = request.form['colorcode']
        color_name = request.form['colorname']
        
        getColor = Color.query.filter(Color.color_code==color_code, Color.color_name==color_name).first()
        if getColor:
            getColor.active_flag = True
            db.session.commit()
        else:
            my_data = Color(color_code=color_code,color_name=color_name)
            db.session.add(my_data)
            db.session.commit()

        flash('Color : "'+color_name+'" has been added !', 'success')
        return redirect(url_for('mcolor.index'))
  
@mcolor.route('/update/<string:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        my_data = Color.query.get(id)
  
        my_data.color_code = request.form.get('colorcode'+id)
        my_data.color_name = request.form.get('colorname'+id)
          
        db.session.commit()
        flash('Color : "'+my_data.color_name+'" has been updated !', 'success')
        return redirect(url_for('mcolor.index'))
  
@mcolor.route('/delete/<string:id>', methods = ['GET', 'POST'])
@login_required
def delete(id):
    if request.method == 'POST':
        my_data = Color.query.get(id)
        my_data.active_flag = False
          
        db.session.commit()
        flash('Color : "'+my_data.color_name+'" has been deleted !', 'success')
        return redirect(url_for('mcolor.index'))