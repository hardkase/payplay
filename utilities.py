from __future__ import print_function
import pandas as pd 
import numpy as np 
import datetime as dt
import constants as con
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import platform

def oscheck():
    osversion = platform.platform()
    return osversion

def feed_pandas(doc):
    data = pd.DataFrame(pd.read_excel(doc))
    return data

def csvmaker(data, name, PATHDATA):
    data.to_csv("{0}{1}{2}{3}".format(PATHDATA[0], PATHDATA[1], name, PATHDATA[4]))

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
            first_run = newjob
            first_run = init_weekly(first_run, jobhandler.date_data)
            # first_list = listify(newjob)
            jobhandler.first_run = first_run
            jobhandler.jobruns.append(first_run) # add series to list
        else:
            current_job = jobhandler.first_run # series
            current_job = run_weekly(current_job, push) # handle series
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
            date_data = jobhandler.date_data
            freq = jobhandler.jobtype
            first_run = init_qtr(newjob, date_data, freq)
            jobhandler.first_run = first_run
            jobhandler.jobruns.append(first_run)
        else:
            current_job = run_qtr(jobhandler.first_run, push)
            current_job = build_summary(current_job)
            jobhandler.jobruns.append(current_job)
    return jobhandler

def init_list_weekly(newjob, date_data):
    for i in range(len(newjob)):
        value = newjob[i]
        if con.FINAL_COLUMNS[i] in con.TARGETS:
            value = get_weekly_date(value, date_data)
        newjob[i] = value
        newjob = build_summary(newjob)
    return newjob

def init_weekly(newjob, date_data):
    for i in range(len(newjob.index)):
        value = newjob[i]
        if newjob.index[i] in con.TARGETS:
            value = get_weekly_date(value, date_data)
        newjob[i] = value
        newjob = build_summary(newjob)
    return newjob

def run_weekly_list(first_list, push):
    nextwk = first_list
    for c in range (len(nextwk)):
        value = nextwk[c]
        if con.FINAL_COLUMNS[c] in con.TARGETS:
            change = 7 * push
            value = value + relativedelta(days=+change)
            nextwk[c] = value
            nextwk = build_summary(nextwk)
        return nextwk
        
def run_weekly(first_run, push):
    nextwk = first_run
    for c in range (len(nextwk.index)):
        value = nextwk[c]
        if first_run.index[c] in con.TARGETS:
            change = 7 * push
            value = value + relativedelta(days=+change)
            nextwk[c] = value
            nextwk = build_summary(nextwk)
        return nextwk

def init_monthly(newjob):
    pass

def run_monthly(first_run, push):
    pass

def init_qtr(newjob, date_data, freq):
    year = date_data[1]
    qtr = date_data[5]
    qtr_data = get_qtr(qtr)
    qtr_month = qtr_data[1]
    for j in range(len(newjob.index)):
        if newjob.index[j] in con.TARGETS:
            if freq == "quarterly-after":
                qtr_data = get_qtr_aft(qtr)
                qtr_month = qtr_data[0]
            else:
                qtr_data = get_qtr(qtr)
                qtr_month = qtr_data[1]
            value = newjob[j]
            if isinstance(value, str):
                if "lwd" in value:
                    lwd = get_lwd(qtr_month, year)
                    newdate = date_builder(year, qtr_month, lwd)
                    newjob[j] = newdate
            elif isinstance(value, int):
                newdate = date_builder(year, qtr_month, value)
                newjob[j] = newdate
    return newjob

def run_qtr(first_run, push):
    nextjob = first_run
    for j in range(len(nextjob.index)):
        if nextjob.index[j] in con.TARGETS:
            if isinstance(nextjob[j], dt.date):
                modifier = 3 * push
                newdate = nextjob[j] + relativedelta(months=+modifier)
                nextjob[j] = newdate
    return nextjob


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

def get_qtr(qtr):
    qtr_data = con.QUARTERS.get(qtr)
    return qtr_data

def get_qtr_aft(qtr):
    qtr = qtr + 1
    if qtr > 4:
        qtr = qtr - 4
    qtr_data = get_qtr(qtr)
    return qtr_data
    
def build_summary(job):
    client = job[1]
    freq = job[2]
    pay = job[3]
    summary = "{0} - {1} - {2}".format(client, freq, pay)
    job[0] = summary
    return job

def get_lwd(month, year):
    value = monthrange(year, month)
    lwd = value[1]
    return lwd

def date_builder(year, month, day):
    try:
        newdate = dt.date(year, month, day)
    except ValueError as er1:
        print("INPUTS INCORRECT", er1)
        newdate = "NULL"
    except ValueError as er2:
        print("INPUTS INCORRECT", er2)
        newdate = "NULL"
    return newdate

def listify(job):
    newlist = []
    for z in range(len(job.index)):
        newlist.append(job[z])
    for item in newlist:
        print("DEBUG - LIST! ", item)
    print("LEN OF LIST", len(newlist))
    print("LEN OF JOB SERIES ", len(job.index))
    return newlist


