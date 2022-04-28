from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from .utils import load_menu

views = Blueprint('views', __name__)

@views.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))

@views.route('/home')
@login_required
def home():    
    menus = load_menu(current_user.user_group)
    return render_template('home.html', user=current_user, menus=menus)

@views.route('/about')
@login_required
def about():
    menus = load_menu(current_user.user_group)
    return render_template('about.html', user=current_user, menus=menus)

@views.route('/test')
@login_required
def test():
    menus = load_menu(current_user.user_group)
    return render_template('test.html', user=current_user, menus=menus)

