# hoodcast

# Hoodcast

---

---

### `import hoodflex as hf`

```python
import datetime as dt
from dateutil.relativedelta import relativedelta

import hoodflex as hf

%matplotlib inline
%matplotlib widget
```

---

### Set parameters

for `Robbin`

```python
ticker = 'IDEX'
# dates = [dt.datetime.now()-relativedelta(months=6), dt.datetime(2020, 11, 24), dt.datetime(2021, 1, 25)]
dates = [dt.datetime(2021, 1, 5), dt.datetime(2021, 1, 11), \
         dt.datetime(2021, 1, 14), dt.datetime(2021, 1, 25), \
         dt.datetime(2021, 2, 4), dt.datetime(2021, 2, 8)]
```

---

#### Create instantiations of `Robbin`

```python
robb = hf.Robbin(ticker, date_points=dates)
```

---

#### `Robbin`

```python
app_layout = robb.hoodflex_widget()
display(app_layout)
```

AppLayout(children=(SelectionRangeSlider(description='Date:', index=(30, 60), layout=Layout(grid_area='footer'…

---

### Set parameters

for `Mobbin`

```python
companies_list = ['Ideanomics, Inc.', 'Tesla, Inc.', 'Amazon Com Inc', 'Apple Inc', \
                  'Aptose Biosciences Inc.', 'XPENG INC.', 'DPW Holdings, Inc.']
company_name = companies_list[0]
form = '10-Q'
year = '2020'
```

---

#### Create instantiation of `Mobbin`

```python
mobb = hf.Mobbin(company_name, form, year)
```

---

---

#### `Mobbin`

```python
df_array, file_array, table_titles, engine, session = mobb.statements_to_sql()
```

---

---

---

### Query search

---

#### Current ratio (Working capital ratio)

```python
current_assets = session.execute("SELECT * FROM Balance WHERE account='Total current assets'").fetchall()
tca_recent = current_assets[0][2]
current_liabilities = session.execute("SELECT * FROM Balance WHERE account='Total current liabilities'").fetchall()
tcl_recent = current_liabilities[0][2]
ratio = tca_recent / tcl_recent
string = format_string(ratio)
string
```

'3.24:1 ratio'

#### Debt ratio

```python
total_assets = session.execute("SELECT * FROM Balance WHERE account='Total assets'").fetchall()
ta_recent = total_assets[0][2]
total_liabilities = session.execute("SELECT * FROM Balance WHERE account='Total liabilities'").fetchall()
tl_recent = total_liabilities[0][2]
ratio = ta_recent / tl_recent
string = format_string(ratio)
string
```

'4.06:1 ratio'

#### Acid-test ratio (Quick Ratio)

```python
current_assets = session.execute("SELECT * FROM Balance WHERE account='Total current assets'").fetchall()
ca_recent = current_assets[0][2]
current_liabilities = session.execute("SELECT * FROM Balance WHERE account='Total current liabilities'").fetchall()
cl_recent = current_liabilities[0][2]
accounts_receivables = session.execute("SELECT * FROM Balance WHERE account='Accounts receivable'").fetchall()
ar_recent = accounts_receivables[0][2]
cash = session.execute("SELECT * FROM Balance WHERE account='Cash and cash equivalents'").fetchall()
cash_recent = cash[0][2]
ratio = (cash_recent+ca_recent+ar_recent) / cl_recent
string = format_string(ratio)
string
```

'6.23:1 ratio'

#### Debt-equity (D/E) ratio

```python
total_liabilities = session.execute("SELECT * FROM Balance WHERE account='Total liabilities'").fetchall()
tl_recent = total_liabilities[0][2]
total_sh_equity = session.execute("SELECT * FROM Balance WHERE account='Total equity'").fetchall()
tshe_recent = total_sh_equity[0][2]
ratio = tl_recent / tshe_recent
string = format_string(ratio)
string
```

'3.03:1 ratio'

#### EPS

```python
net_income = session.execute("SELECT * FROM Income WHERE account='Net loss'").fetchall()
ni_recent = net_income[0][2]
pref_dividends = session.execute("SELECT * FROM Balance WHERE account='Series A'").fetchall()
pf_recent = pref_dividends[0][2]
count_table = session.execute("SELECT COUNT(*) FROM Equity").fetchall()
count = count_table[-1][-1]
common_shares = session.execute("SELECT * FROM Equity").fetchall()
cso_recent = common_shares[count-1][2]
ratio = (ni_recent-pf_recent) / cso_recent
string = format_string(ratio)
string
```

'≈0:1 ratio'

```python
if not net_income:
    print('yes')
```

#### Price-earnings (P/E) ratio

```python
ratio = df_yahoo.Close[-1] / ratio
string = format_string(ratio)
string
```

'-640011:1 ratio'

#### Return on Equity (ROE)

```python
net_income = session.execute("SELECT * FROM Income WHERE account='Net loss'").fetchall()
ni_recent = net_income[0][2]
total_sh_equity = session.execute("SELECT * FROM Balance WHERE account='Total equity'").fetchall()
tshe_recent = total_sh_equity[0][2]
ratio = ni_recent / tshe_recent
string = format_string(ratio)
string
```

yes

#### Price-to-book ratio (P/B)

#### \--Book value per common share (BVPS) for P/B ratio

```python
total_sh_equity = session.execute("SELECT * FROM Balance WHERE account='Total equity'").fetchall()
tshe_recent = total_sh_equity[0][2]
preferred = session.execute("SELECT * FROM Balance WHERE account='Non-controlling interest'").fetchall()
pre_recent = preferred[0][2]
common_shares = session.execute("SELECT * FROM Equity").fetchall()
cso_recent = common_shares[count-1][2]
ratio = (tshe_recent-pre_recent) / cso_recent
string = format_string(ratio)
string
count
```

34

#### \--P/B ratio

```python
ratio = df_yahoo.Close[-1] / ratio
string = format_string(ratio)
string
```

'3084:1 ratio'

#### Working capital turnover

```python
current_assets = session.execute("SELECT * FROM Balance WHERE account='Total current assets'").fetchall()
ca_recent = current_assets[0][2]
current_liabilities = session.execute("SELECT * FROM Balance WHERE account='Total current liabilities'").fetchall()
cl_recent = current_liabilities[0][2]
total_revenue = session.execute("SELECT * FROM Operations WHERE account='Total revenue'").fetchall()
tr_recent = total_revenue[0][2]
ratio = (ca_recent-cl_recent) / tr_recent
string = format_string(ratio)
string
```

'8.28:1 ratio'

---

---

---

---

