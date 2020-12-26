from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, ZipChoice, DeleteForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Listing
from flask_login import login_required
from werkzeug.urls import url_parse
import os
from sqlalchemy import desc
import pandas as pd


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ZipChoice()
    if form.validate_on_submit():
        zip = form.zipcode.data
        return redirect(url_for('zipsearch', zipcode=zip))
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        
        #This logic is to help move a user to the page they were after they log in
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/search/<zipcode>")
@login_required
def zipsearch(zipcode):
    #Query and Pagination work
    page = request.args.get('page', 1, type=int)
    search_results = Listing.query.filter_by(zipcode=zipcode).order_by(desc(Listing.price)).paginate(
        page, app.config['LISTINGS_PER_PAGE'], False)
    next_url = url_for('zipsearch', page=search_results.next_num, zipcode=zipcode) \
        if search_results.has_next else None
    prev_url = url_for('zipsearch', page=search_results.prev_num, zipcode=zipcode) \
        if search_results.has_prev else None

    search_results_df = Listing.query.filter_by(zipcode=zipcode)
    df = pd.read_sql(search_results_df.statement, search_results_df.session.bind)
    print (df)
    
    return render_template('zipsearch.html', title='Results', search_results=search_results, zipcode=zipcode, next_url=next_url,
                           prev_url=prev_url)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    all_users = User.query.all()
    if request.method == 'POST':
        post_id = request.form.get('delete')
        if post_id is not None:
            user = User.query.get(post_id)
            db.session.delete(user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            return redirect(url_for('admin'))
    return render_template('admin.html', title='Admin', all_users=all_users)


#The below code is so the css style does not cache
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)