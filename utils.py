# utils
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

def build_summary(job):
    print("DEBUG LEN: {0}, VAL: {1}".format(len(job), job))
    client = job[1]
    freq = job[2]
    pay = job[3]
    summary = "{0} - {1} - {2}".format(client, freq, pay)
    job[0] = summary
    return job

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
            last = get_lwd(jobd_data[0], job_data[1])
        elif stringer and "-" in value:
            last = get_lwd(jobd_data[0], job_data[1])
            value = value.strip()
            value = re.sub(" ", "", value)
            valist = re.split("-", value)
            modifier = valist[1]
            whiskey = last - modifier
    else:
        whiskey = 0
    return whiskey

