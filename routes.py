from sqlalchemy import asc, desc, func, distinct, column, sql
from flask import request, render_template, flash, redirect, url_for
from models import Company, Statement
from forms import SearchForm, SearchResults
from werkzeug.urls import url_parse
from app import app, db
import datetime as dt
import hoodflex as hf


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    companies = Company.query.with_entities(Company.title).all()
    
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        form_type = form.form_type.data
        year = form.year.data
        next_page = request.args.get('next')
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('metrics', name=name, form_type=form_type, 
                                year=year, table='Balance', sort='new', 
                                col_index=1)
        return redirect(next_page)
    return render_template('landing_page.html', 
                           form=form, companies=companies)


@app.route('/MOBBIN/<name>/<form_type>/<year>/<table>/<sort>/<col_index>', 
           methods=['GET', 'POST'])
def metrics(name, form_type, year, table, sort, col_index):
    current = dt.datetime.now()
    date_array = [current]
    company = Company.query.filter_by(title=name).first()
    statement = Statement.query.filter_by(company=name).first()

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
    
    table_list = ['Balance', 'Income', 'Operation', 'Equity', 'Cash']
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
    
    columns = session.execute(f"SELECT * FROM {table}").keys()
    
    if sort != 'new':
        df = session.execute(f"SELECT * FROM {table} ORDER BY `{columns[int(col_index)]}` {sort}").fetchall()
    else:
        df = session.execute(f"SELECT * FROM {table}").fetchall()
        
    ratios = SearchResults(mobb, robb, session)
    form = SearchForm()
    companies = Company.query.with_entities(Company.title).all()
    
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        form_type = form.form_type.data
        year = form.year.data
        next_page = request.args.get('next')
        table = request.args.get('table') 
        sort = request.args.get('sort') 
        col_index = request.args.get('col_index')
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('metrics', name=name, form_type=form_type, 
                                year=year, table='Balance', sort='new', 
                                col_index=1)
            
        return redirect(next_page)
    
    return render_template('metrics.html', form=form, name=name, 
                           form_type=form_type, year=year, table=table, 
                           sort=sort, col_index=col_index, company=company, 
                           ratios=ratios, table_titles=table_titles, 
                           df=df, columns=columns, companies=companies)
