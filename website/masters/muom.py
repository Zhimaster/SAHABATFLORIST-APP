from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import true
from wtforms import Form, StringField, validators
from website import db
from website.utils import load_menu
from website.models import Uom

muom = Blueprint('muom', __name__)

# Master UOM Form Class
class MasterUomForm(Form):
    uomcode = StringField(None,'UOM Code', [
        validators.DataRequired(),
        validators.Regexp('^[A-Z]+$',0,'First Name only allow Alphabet characters.'),
        validators.Length(min=1, max=10)])
    uomname = StringField(None,'UOM Name', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'Last Name only allow Alphabet characters.'),
        validators.Length(min=1, max=30),])
    
@muom.route('/')
@login_required
def index():
    menus = load_menu(current_user.user_group)
    form = MasterUomForm(request.form)
    all_data = Uom.query.filter_by(active_flag=True).order_by(Uom.uom_code).all()
    return render_template('masters/muom.html', user=current_user, menus=menus, muoms=all_data, form=form)

@muom.route('/insert', methods = ['POST'])
@login_required
def insert():
    if request.method == 'POST':
        uomcode = request.form['uomcode']
        uomname = request.form['uomname']
        
        getData = Uom.query.filter(Uom.uom_code==uomcode, Uom.uom_name==uomname).first()
        if getData:
            getData.active_flag = True
            db.session.commit()
        else:
            my_data = Uom(uom_code=uomcode,uom_name=uomname)
            db.session.add(my_data)
            db.session.commit()

        flash('UOM : "'+uomname+'" has been added !', 'success')
        return redirect(url_for('muom.index'))
  
@muom.route('/update/<string:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        my_data = Uom.query.get(id)
  
        my_data.uom_code = request.form.get('uomcode'+id)
        my_data.uom_name = request.form.get('uomname'+id)
          
        db.session.commit()
        flash('Uom : "'+my_data.uom_name+'" has been updated !', 'success')
        return redirect(url_for('muom.index'))
  
@muom.route('/delete/<string:id>', methods = ['GET', 'POST'])
@login_required
def delete(id):
    if request.method == 'POST':
        my_data = Uom.query.get(id)
        my_data.active_flag = False
          
        db.session.commit()
        flash('Uom : "'+my_data.uom_name+'" has been deleted !', 'success')
        return redirect(url_for('muom.index'))