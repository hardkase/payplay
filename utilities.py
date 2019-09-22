import pandas as pd 
import numpy as np 
import datetime as dt
import constants as con
from dateutil.relativedelta import relativedelta
from calendar import monthrange

def csvmaker(data, name):
    data.to_csv("{0}{1}{2}{3}".format(con.PATHDATA[0], con.PATHDATA[1], name, con.PATHDATA[4]))

def fix_columns(data):
    data.columns = con.COLUMN_NAMES
    return data

def insert_column(data, index_pos, col_name, value):
    data = data.insert(index_pos, col_name, value)
    return data

def to_lower(data):
    # there has to be an easier way to do this ...
    for i in range(len(data.index)):
        series = data.iloc[i]
        series.str.lower
        for j in range(len(series.index)):
            val = series[j]
            if isinstance(val, str):
                series[j] = val.lower()
        data.iloc[i] = series
        print("DEBUG: ", series)
    return data

# YES, could simplify this to one function 'process', push range values to a dict in constants
# and pass in range values based on jobtype...maybe later
def process_weekly(jobhandler):
    newjob = jobhandler.job
    for a in range(0, 52):
        push = a
        if a < 1:
            first_run = listify(newjob)
            first_run = init_weekly(newjob, jobhandler.date_data)
            jobhandler.first_run = first_run
            jobhandler.jobruns.append(first_run)
        else:
            current_job = run_weekly(jobhandler.first_run, push)
            jobhandler.jobruns.append(current_job)
    return jobhandler

def process_monthly(jobhandler):
    newjob = jobhandler.job
    for a in range(0, 12):
        push = a
        if a < 1:
            first_run = init_monthly(newjob)
            jobhandler.first_run = first_run
            jobhandler.jobruns.append(first_run)
        else:
            current_job = run_monthly(jobhandler.first_run, push)
            jobhandler.jobruns.append(current_job)
    return jobhandler

def process_qtr(jobhandler):
    newjob = jobhandler.job
    for a in range(0, 4):
        push = a
        if a < 1:
            first_run = init_qtr(newjob)
            jobhandler.first_run = first_run
            jobhandler.jobruns.append(first_run)
        else:
            current_job = run_qtr(jobhandler.first_run, push)
            jobhandler.jobruns.append(current_job)
    return jobhandler

def process_qtr_aft(jobhandler):
    newjob = jobhandler.job
    for a in range(0, 4):
        push = a
        if a < 1:
            first_run = init_qtr_aft(newjob, jobhandler.date_data)
            jobhandler.first_run = first_run
            jobhandler.jobruns.append(first_run)
        else:
            current_job = run_qtr_aft(jobhandler.first_run, push)
            jobhandler.jobruns.append(current_job)
    return jobhandler

def init_weekly(newjob, date_data):
    for i in range(len(newjob)):
        value = newjob[i]
        if con.FINAL_COLUMNS[i] in con.TARGETS:
            value = get_weekly_date(value, date_data)
        newjob[i] = value
        newjob = build_summary(newjob)
    return newjob

def run_weekly(first_run, push):
    for c in range (len(first_run.index)):
        nextwk = first_run
        value = nextwk[c]
        if con.FINAL_COLUMNS[c] in con.TARGETS:
            change = 7 * push
            value = value + relativedelta(days=+change)
            nextwk[c] = value
            nextwk = build_summary(nextwk)
        return nextwk
        

def init_monthly(newjob):
    pass

def run_monthly(first_run, push):
    pass

def init_qtr(newjob):
    pass

def run_qtr(first_run, push):
    pass

def init_qtr_aft(newjob):
    pass

def run_qtr_aft(first_run, push):
    pass

def get_weekly_date(value, date_data):
    if value in con.WEEKDAYLIST:
        paywkdaylist = [number for number, weekday in con.WEEKDAYS.items() if weekday == value]
        paywkday = paywkdaylist.pop()
        print("DEBUG : WEEKDAY NUMBER: ", paywkday)
        # return wkday value from con
        print("paywekday - val: {0}\ttype: {1}\ncurrent val: {2}\ttype: {3}".format(paywkday, type(paywkday), date_data[4], type(date_data[4])))
        daydiff = (paywkday - date_data[4]) + 7
        payday = date_data[0] + relativedelta(days=+daydiff)
        print("DEBUG REJIGGED PAY DATE: ", payday)
        value = payday
        # payday - current wkday
        # day = 
    else:
        value = value
    return value

def build_summary(job):
    client = job[1]
    freq = job[2]
    pay = job[3]
    summary = "{0} - {1} - {2}".format(client, freq, pay)
    job[0] = summary
    return job

def listify(job):
    newlist = []
    for z in range(len(job.index)):
        newlist.append(job[z])
    for item in newlist:
        print("DEBUG - LIST! ", item)
    print("LEN OF LIST", len(newlist))
    print("LEN OF JOB SERIES ", len(job.index))
    return newlist


