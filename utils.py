# utils
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import cons
import re

def handle_qtr(job, datedata, after):
    qtr = datedata[5]
    get_qtr_month = 1
    if after:
        qtr = qtr + 1
        if qtr > 4:
            qtr = qtr - 4
        get_qtr_month = 0
    qtr_data = get_qtr(qtr)
    job_data = [datedata[1], qtr_data[get_qtr_month]]  #year, qtr_month
    joblist = cons.TEMPLATE
    for a in range(len(job.index)):
        if job.index[a] in cons.TARGETS:
            value = job[a]
            value = value_checker(value, job_data)
            paydate = datebuilder(datedata[1], qtr_data[get_qtr_month], value)
            joblist.append(paydate)
        else:
            joblist.append(job[a])
            # DEBUG shows jumping from iteration 1 to build summary, so logic funky somwehre here
        joblist = build_summary(joblist)
    print(joblist)
    return joblist

def run_qtr_jobs(job, push):
    modifier = push * 3
    for i in range(len(job)):
        if i in [3,4,5]:
            job[i] = job[i] + relativedelta(month=+modifier)
        job = build_summary(job)
        return job

def stringcheck(value):
    isastr = False
    if isinstance(value, str):
        isastr = True
    return isastr

def intcheck(value):
    isnumber = False
    if isinstance(value, int):
        isnumber = True
    return isnumber

def hiding_number(value):
    actnum = False
    if isinstance(value, str):
        if value.isdigit():
            actnum = True
            print("AH-HAH!!", value)
    return actnum

def scoop_num(value):
    value = int(value)
    return value

def datebuilder(year, month, day):
    error = False
    try:
        newdate = dt.date(year, month, day)
    except ValueError as er1:
        print("Value Error: ", er1)
        error = True
    except TypeError as er2:
        print("Type Error: ", er2)
        error = True
    if error:
        newdate = dt.date(1941, 12, 7)
    return newdate

def build_summary(joblist):
    # print("DEBUG LEN: {0}, VAL: {1}".format(len(job), job))
    client = joblist[1]
    freq = joblist[2]
    pay = joblist[3]
    summary = "{0} - {1} - {2}".format(client, freq, pay)
    joblist[0] = summary
    return joblist

def build_sum(job):
    job.summary = "{0} - {1} - {2}".format(job.client, job.freq, job.paydate, job.current_paydate)

def get_lwd(year, month):
    print("MONTH {0}, YEAR{1}".format(month, year))
    value = monthrange(year, month)
    lwd = value[1]
    return lwd

def get_qtr(qtr):
    qtr_data = cons.QUARTERS.get(qtr)
    return qtr_data

def value_checker(value, job_data):  # We gonna distill us some truth bois
    stringer = isinstance(value, str)
    numero = isinstance(value, int)
    if numero:
        whiskey = value
    elif stringer:
        cloaked_int = value.isdigit()
        if cloaked_int:
            whiskey = int(value)
        if stringer and value == "lwd":
            last = get_lwd(job_data[0], job_data[1])
        elif stringer and "-" in value:
            last = get_lwd(job_data[0], job_data[1])
            value = value.strip()
            value = re.sub(" ", "", value)
            valist = re.split("-", value)
            modifier = valist[1]
            whiskey = last - modifier
    else:
        whiskey = 0
    return whiskey

def handle_weekly(job):
    first_job = job.jobdata
    joblist = listor(first_job)
    print("DEBUG - LENGTH COMPARE SERIES {0} AND LIST {1}".format(len(first_job.index), len(joblist)))
    for b in range(len(first_job.index)):        
        if first_job.index[b] in cons.TARGETS:
            value = joblist[b].strip()
            target_day = get_wkday_val(value)
            daydiff = (target_day - job.weekday) + 7
            firstday = job.today + relativedelta(days=+daydiff)
            joblist[b] = firstday
            job.current_paydate = firstday
            print("CHECK2: ", firstday)
            #Trying to not do else because nothing should change
        else:
            joblist[b] = first_job[b]
        joblist = build_summary(joblist)
        job.first_job = create_series(joblist)
        job.current_job = job.first_job
        job.last_job = job.current_job
        print(job.current_job)
    return job

def get_wkday_val(value):
    valist = [number for number, weekday in cons.WEEKDAYS.items() if weekday == value]
    target_day = valist.pop()
    return target_day

def run_weekly(job):
    current_job = job.last_job
    joblist = listor(current_job)
    for c in range(len(current_job.index)):
        print("DEBUG - JOB IS GOING HERE...")
        # if c in [3,4,5]:
        if current_job.index[c] in cons.TARGETS:
            print("DEBUG AGAIN - IS JOB GOING HERE??")
            value = joblist[c]
            print("ANOTHER DEBUG", value)
            # print("OLD DATE TYPE: {0}, VALUE: {1}".format(type(oldpaydate), oldpaydate))
            value = value + relativedelta(weeks=+1)
            joblist[c] = value
            print("IS VALUE CHANGING???", joblist[c])
            job.current_paydate = value
            # print("NEWDATE TYPE: {0}, VALUE: {1}".format(type(newdate), newdate))
        else:
            joblist[c] = current_job[c]
        print("WHAT DOES JOBLIST LOOK LIKE?>?", joblist)
        joblist = build_summary(joblist)
        print("OK, WHAT DOES JOBLIST LOOK LIKE, NEW SUMMARY?", joblist)
        current = create_series(joblist)
        print("OK, Here's the new Series: ", current)
        job.current_job = current
        job.last_job = current_job
        print(job.last_job)
    return job

def create_series(joblist):
    print("ANOTHER LOOK AT JOBLIST...", joblist)
    jobrun = pd.Series(joblist)
    print("ANOTHER DEBUG - what does the series look like?", jobrun)
    return jobrun

def listor(job):
    print(job.index)
    joblist = []
    for a in range(len(job.index)):
        joblist.append(job[a])
    return joblist

    """
    OK, let's bonk dealing with series, we'll start with a dataframe, split to series for jobs, process all jobs as a list, pass
    lists to alljobs list, take a look -> then see about sending list of jobs back to a DF>GRRRR ARRRGH
    """