import numpy as np
import pandas as pd
import fuckit
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from werkzeug.urls import url_parse
from sqlalchemy import asc, desc, func, distinct, column, sql
from models import Company, Statement, User
from app import app, db


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], 
                        render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], 
                             render_kw={'placeholder': 'Password'})
    password2 = PasswordField('Repeat it', 
                              validators=[DataRequired(), 
                                          EqualTo('password', 
                                                  message='Not a match')], 
                              render_kw={'placeholder': 'Repeat!'})
    submit = SubmitField('LINK!')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], 
                        render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], 
                       render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('LOGIN!')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email invalid')


class SearchForm(FlaskForm):
    name = StringField('Company name', 
                       validators=[DataRequired('As it appears on the SEC website')], 
                       render_kw={'placeholder': 'Company name'})
    form_type = StringField('Form', 
                            validators=[DataRequired('Specify form')], 
                            render_kw={'placeholder': 'SEC Form (10-Q, 10-K)'})
    year = StringField('Year', 
                       validators=[DataRequired('Year')], 
                       render_kw={'placeholder': 'Year'})
    submit = SubmitField('MOBB!')
    
    def validate_company(self, name):
        company = Company.query.filter_by(title=name.data).first()
        if company is None:
            raise ValidationError('Invalid company name')

    
class SearchResults(FlaskForm):
    @fuckit
    def __init__(self, mobb, robb, session, mobb_type='mobbin'):

        self.mobb = mobb
        self.df_yahoo = robb.full_dataframe()
        self.price = self.df_yahoo.Close[-1]
        self.tca = session.execute("SELECT * FROM Balance WHERE account='Total current assets'").fetchall()[0][2]
        self.tcl = session.execute("SELECT * FROM Balance WHERE account='Total current liabilities'").fetchall()[0][2]
        self.ta = session.execute("SELECT * FROM Balance WHERE account='Total assets'").fetchall()[0][2]
        self.tl = session.execute("SELECT * FROM Balance WHERE account='Total liabilities'").fetchall()[0][2]
        self.cash = session.execute("SELECT * FROM Balance WHERE account='Cash and cash equivalents'").fetchall()[0][2]
        self.ar = session.execute("SELECT * FROM Balance WHERE account='Accounts receivable'").fetchall()[0][2]
        income = session.execute("SELECT * FROM Income WHERE account='Net income (loss)'").fetchall()
        if not income:
            income = session.execute("SELECT * FROM Income WHERE account='Net income'").fetchall()
        if not income:
            income = session.execute("SELECT * FROM Income WHERE account='Net loss'").fetchall()
        self.ni = income[0][2]
        self.tr = session.execute("SELECT * FROM Operations WHERE account='Total revenue'").fetchall()[0][2]
        self.pf = session.execute("SELECT * FROM Balance WHERE account='Series A'").fetchall()[0][2]
        equity = session.execute("SELECT * FROM Balance WHERE account='Total equity'").fetchall()
        if not equity:
            equity = session.execute("SELECT * FROM Balance WHERE account='Total shareholders’ equity'").fetchall()
        self.tshe = equity[0][2]
        self.tshe = equity - session.execute("SELECT * FROM Balance WHERE account='Non-controlling interest'").fetchall()[0][2]
        count = session.execute("SELECT COUNT(*) FROM Equity").fetchall()[-1][-1]
        self.cso = session.execute("SELECT * FROM Equity").fetchall()[count-1][2]
    
    def format_string(self, ratio):
        try:
            ratio = float('{0:.3f}'.format(ratio))
            if ratio >= 100 or ratio <= -100:
                ratio = round(ratio)
            if ratio == 0:
                string = '≈0:1 ratio'
            else:
                ratio = float('{0:.2f}'.format(ratio)) if ratio % 1 != 0 else int(ratio)
                if ratio == 0:
                    string = '≈0:1 ratio'
                elif ratio <= -1.0:
                    string = f'-{-ratio}:1 ratio'
                elif ratio < 0.0 and ratio > -1.0:
                    formatted = float("{0:.2f}".format(-1/ratio))
                    string = f'-1:{formatted} ratio' if formatted % 1 != 0 else f'-1:{int(formatted)} ratio'
                elif ratio >= 1.0:
                    string = f'{ratio}:1 ratio'
                else:
                    formatted = float("{0:.2f}".format(1/ratio))
                    string = f'{formatted}:1 ratio' if formatted % 1 != 0 else f'1:{int(formatted)} ratio'
        except:
            string = '-'
        return string
    
    @fuckit
    def get_ratio(self):
        wc, debt, quick, de, eps, pe, roe, pb, wct = ['-'] * 9
        wc = self.format_string(self.tca / self.tcl)
        debt = self.format_string(self.ta / self.tl)
        quick = self.format_string((self.cash+self.tca+self.ar) / self.tcl)
        de = self.format_string(self.tl / self.tshe)
        eps = self.format_string((self.ni-self.pf) / self.cso)
        pe = self.format_string(self.price / ((self.ni-self.pf) / self.cso))
        roe = self.format_string(self.ni / self.tshe)
        pb = self.format_string(self.price / (self.tshe / self.cso))
        wct = self.format_string((self.tca-self.tcl) / self.tr)
        return [wc, debt, quick, de, eps, pe, roe, pb, wct]
