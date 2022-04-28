from unicodedata import category
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import true, column, text
from wtforms import Form, StringField, validators, SelectField
from website import db
from website.utils import get_data_scalar_by_id, load_menu, get_subq
from website.models import Item, Category, Color, Uom, Status

mitem = Blueprint('mitem', __name__)

# Master Item Form Class
class MasterItemForm(Form):
    itemid = StringField(None, 'Item ID')
    itemname = StringField(None,'Item Name', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'Last Name only allow Alphabet characters.'),
        validators.Length(min=1, max=30),])
    itemtype = StringField(None,'Item Type', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'Last Name only allow Alphabet characters.'),
        validators.Length(min=1, max=30),])
    
    itemcats = (Category.query.filter(Category.active_flag==True).all())
    choices1 = []
    for i in itemcats:
        choices1.append((i.category_id,i.category_code+' - '+i.category_name))
    itemcategory = SelectField(None,'Item Category', choices=choices1)

    itemcolors = (Color.query.filter(Color.active_flag==True).all())
    choices2 = []
    for i in itemcolors:
        choices2.append((i.color_id,i.color_code+' - '+i.color_name))
    itemcolor = SelectField(None,'Item Color', choices=choices2)

    itemuoms = (Uom.query.filter(Uom.active_flag==True).all()) 
    choices3 = []
    for i in itemuoms:
        choices3.append((i.uom_code,i.uom_code+' - '+i.uom_name))
    itemuom = SelectField(None,'Item UOM', choices=choices3)

@mitem.route('/')
@login_required
def index():
    menus = load_menu(current_user.user_group)
    form = MasterItemForm(request.form)
    
    all_data = (db.session.query(Item.item_id,Item.item_code,Item.item_name,Item.uom_code,Item.item_type,
                                 get_subq(Category,'name',Item.category_id).label('category_name'),
                                 get_subq(Color,'name',Item.color_id).label('color_name'),
                                 get_subq(Status,'name',Item.status_id).label('status_name')
                                )
            .filter(Item.active_flag==True)
            .order_by(Item.item_id)
            .all())                         
    
    return render_template('masters/mitem.html', user=current_user, 
                            menus=menus, mitems=all_data, form=form)

@mitem.route('/insert', methods = ['POST'])
@login_required
def insert():
    if request.method == 'POST':
        itemname = request.form['itemnamenew']
        itemtype = request.form['itemtypenew']
        categoryid = request.form.get('itemcategorynew')
        colorid = request.form.get('itemcolornew')
        uomcode = request.form.get('itemuomnew')        
        
        getItem = Item.query.filter(Item.item_name==itemname).first()
        if getItem:
            getItem.active_flag = True
            db.session.commit()
        else:
            my_data = Item(item_name=itemname,item_type=itemtype,
                           category_id=categoryid,color_id=colorid,uom_code=uomcode)
            db.session.add(my_data)
            db.session.commit()

        flash('Item : "'+itemname+'" has been added !', 'success')
        return redirect(url_for('mitem.index'))
  
@mitem.route('/update/<string:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        my_data = Item.query.get(id)
  
        my_data.item_name = request.form.get('itemname'+id)
        my_data.category_id = request.form.get('itemcategory'+id)
        my_data.color_id = request.form.get('itemcolor'+id)
        my_data.item_type = request.form.get('itemtype'+id)
        my_data.uom_code = request.form.get('itemuom'+id)
          
        db.session.commit()
        flash('Item : "'+my_data.item_name+'" has been updated !', 'success')
        return redirect(url_for('mitem.index'))
  
@mitem.route('/delete/<string:id>', methods = ['GET', 'POST'])
@login_required
def delete(id):
    if request.method == 'POST':
        my_data = Item.query.get(id)
        if my_data.status_id == 0:
            my_data.active_flag = False  
            db.session.commit()
            flash('Item : "'+my_data.item_name+'" has been deleted !', 'success')
        else:
            flash('Item : "'+my_data.item_name+'" can''t be deleted !', 'danger')
        
        return redirect(url_for('mitem.index'))
    
@mitem.route("/genitemname",methods=["POST","GET"])
def genitemname():  
    if request.method == 'POST':        
        category_id = request.form.get('category_id')
        item_type = request.form.get('item_type')
        color_id = request.form.get('color_id')
        
        category_code = get_data_scalar_by_id(Category,'category_code',category_id)
        color_code = get_data_scalar_by_id(Color,'color_code',color_id)
                
        result = category_code + ' ' + item_type + ' ' + color_code
        
        return result