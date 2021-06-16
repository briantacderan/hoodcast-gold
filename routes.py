from sqlalchemy import asc, desc, func, distinct, column, sql
from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required
from models import Company, Statement, User
from forms import RegistrationForm, LoginForm, SearchForm, SearchResults
from werkzeug.urls import url_parse
from app import app, db
import datetime as dt
import hoodflex as hf


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        if form.remember_me.data:
            login_user(user, remember=True)
        else:
            login_user(user)
        flash('Logged in successfully')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', current_user=current_user)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    companies_tuple = Company.query.with_entities(Company.title).all()
    companies = []
    for company in companies_tuple:
        companies.append(company[0])
    
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        form_type = form.form_type.data
        year = form.year.data
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('metrics', name=name, form_type=form_type, 
                                year=year)
        return redirect(next_page)
    return render_template('landing_page.html', 
                           form=form, companies=companies)


@app.route('/mobbin-results/<name>/<form_type>/<year>', methods=['GET', 'POST'])
@login_required
def metrics(name, form_type, year):
    company = Company.query.filter_by(title=name).first()
    statement = Statement.query.filter_by(company_id=company.id).first()
    current = dt.datetime.now()
    date_array = [current]

    for i in range(5):
        fortnite = dt.timedelta(days=14)
        current += fortnite
        date_array.append(current)

    try:
        mobb = hf.Mobbin(name, form_type, year)
    except:
        flash('Certain form requests may be unavailable')
        return redirect(url_for('index'))

    try:
        robb = hf.Robbin(company.ticker, date_points=date_array)
    except:
        flash('Some financial metrics unavailable')

    df_array, file_array, table_titles, engine, session = \
    mobb.statements_to_sql()
    
    table_list = ['Balance', 'Income', 'Operations', 'Equity', 'Cash']
    sort_list = ['new', 'asc', 'desc']
    bala, inco, oper, equi, cash = [None] * 5
    table_val = [bala, inco, oper, equi, cash]
    
    if file_array:
        for i in range(len(table_titles)):
            for j in range(len(table_list)):
                table_val[i] = file_array[i] \
                if table_titles[i] == table_list[j] \
                else table_val[i]

    if statement is None:
        statement = Statement(form_type=form_type,
                              year=year,
                              company=name,
                              bs=bala,
                              income=inco,
                              ops=oper,
                              equity=equi,
                              cash=cash,
                              company_id=company.id)

        db.session.add(statement)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return redirect(url_for('index'))
    
    df_dict = {}
    
    for i in range(len(table_titles)):
        df_dict[table_titles[i]] = {}
        columns = list(session.execute(f"SELECT * FROM {table_titles[i]}").keys())
        df_dict[table_titles[i]]['columns'] = columns

        for j in range(len(sort_list)):

            for k in range(len(columns)):
                dict_str = f"col_{k}_{sort_list[j]}"
                if j == 0 and k > 0:
                    continue
                elif j == 0:
                    df_dict[table_titles[i]]['new'] = \
                    session.execute(f"SELECT * FROM {table_titles[i]}")\
                    .fetchall()
                else:
                    df_dict[table_titles[i]][dict_str] = \
                    session.execute(f"SELECT * FROM {table_titles[i]} ORDER BY `{columns[k]}` {sort_list[j]}").fetchall()

        df_dict[table_titles[i]]['keys_list'] = \
        list(df_dict[table_titles[i]].keys())

    ratios = SearchResults(mobb, robb, session)
    form = SearchForm()
    companies_tuple = Company.query.with_entities(Company.title).all()
    companies = []
    for company in companies_tuple:
        companies.append(company[0])
    
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        form_type = form.form_type.data
        year = form.year.data
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('metrics', name=name, form_type=form_type, 
                                year=year)
        return redirect(next_page)
    
    return render_template('metrics.html', form=form, name=name, 
                           form_type=form_type, year=year, company=company, 
                           ratios=ratios, table_titles=table_titles, 
                           columns=columns, companies=companies,
                           session=session, df_dict=df_dict, 
                           scrollToAnchor='head')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
