import numpy as np
import pandas as pd
from app import db
from models import Company, Statement
import os


if os.path.exists('hoodcast.db'):
    os.remove('hoodcast.db')
db.create_all()


company_table = pd.read_csv('static/resources/data/edgar_list.csv')

for i in range(len(company_table)):
    
    company = None
    row = company_table.iloc[i]
    row_array = []
    
    while company is None:
        for j in range(len(row)):
            
            if j == 0:
                row_array.append(row[j])
            elif j == 1:
                company = Company.query.filter_by(ticker=row[j]).first()
                row_array.append(row[j])
            else:
                name = row[j].lower().title()
                company = Company.query.filter_by(title=name).first() 
                row_array.append(name)

                post_array = Company(cik_str=row_array[0], 
                                     ticker=row_array[1],
                                     title=row_array[2])
                db.session.add(post_array)

                try:
                    db.session.commit()
                except Exception:
                    db.session.rollback()

                break
        break

        
db.session.close()
