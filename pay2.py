# pay2.py 
import pandas as pd
import numpy as np
import datetime as dt 
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import re

data = pd.DataFrame(pd.read_excel("~/payplay/payplay/fakepay2.xlsx"))
today = dt.date.today()
wkday = today.weekday()
qtr = pd.Timestamp(today).quarter
datedata = (today, today.year, today.month, today.day, wkday, qtr)
# clean
print(data.columns)
newcols = ["CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
print(newcols)
data.columns = newcols
print(data)
data = data.apply(lambda x: x.astype(str).str.lower())
print(data)
newcolz = ["SUMMARY"]
for item in newcols:
    newcolz.append(item)
#
data = data.reindex(newcolz, index="columns")
val = ["Summary Here"]
# data = data.insert(0, 'SUMMARY', val, True)
print(data)