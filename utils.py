# utils
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import cons
import re

def handle_qtr(job, after):
    first_job = job.jobdata
    qtr = job.qtr
    get_qtr_month = 1
    if after:
        qtr = qtr + 1
        if qtr > 4:
            qtr = qtr - 4
        get_qtr_month = 0
    qtr_data = get_qtr(qtr)
    job_data = [job.year, qtr_data[get_qtr_month]]  #year, qtr_month
    current_job = []
    for a in range(len(job.idx)):
        if job.idx[a] in cons.TARGETS:
            value = first_job[a]
            value = value_checker(value, job_data)
            paydate = datebuilder(job_data[0], qtr_data[get_qtr_month], value)
            current_job.append(paydate)
            job.current_paydate = paydate
        else:
            current_job.append(first_job[a])
            # DEBUG shows jumping from iteration 1 to build summary, so logic funky somwehre here
    current_job[0] = build_summary(job)
    job.current_job = current_job
    job.last_job = job.current_job
    print("Another bloody check - current job should be good", current_job)
    return job

def run_qtr_jobs(job):
    current_job = job.last_job
    for i in range(len(job.idx)):
        if job.idx[i] in cons.TARGETS:
            print("Test we're getting here")
            print("old date", current_job[i])
            new_date = current_job[i] + relativedelta(months=+3)
            print("new date", new_date)
            current_job[i] = new_date
            job.current_paydate = new_date
        # since we're re-using the list, try not to else this one
    current_job[0] = build_summary(job)
    job.current_job = current_job
    job.last_job = job.current_job
    print("Another bloody check - current job should be good", current_job)
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
    # print("DEBUG LEN: {0}, VAL: {1}".format(len(job), job))
    client = job.client
    freq = job.freq
    pay = job.current_paydate
    summary = "{0} - {1} - {2}".format(client, freq, pay)
    return summary

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
    first_job = job.current_job
    current_job = []
    print("DEBUG - LENGTH COMPARE SERIES {0} AND LIST {1}".format(len(job.jobdata.index), len(first_job)))
    print("check start job: ", first_job)
    for b in range(len(job.idx)):        
        if job.idx[b] in cons.TARGETS:
            value = first_job[b].strip()
            target_day = get_wkday_val(value)
            print("Target day value: ", target_day)
            daydiff = (target_day - job.weekday) + 7
            print("Daydiff value: ", daydiff)
            firstday = job.today + relativedelta(days=+daydiff)
            current_job.append(firstday)
            job.current_paydate = firstday
            print("CHECK1", job.current_paydate)
            #Trying to not do else because nothing should change
            print("Check Job: ", current_job)
        else:
            current_job.append(first_job[b])
        current_job[0] = build_summary(job)
        job.current_job = current_job
        job.last_job = job.current_job
        print("Another bloody check - current job should be good", current_job)
        print(job.current_job)
    return job

def get_wkday_val(value):
    valist = [number for number, weekday in cons.WEEKDAYS.items() if weekday == value]
    target_day = valist.pop()
    return target_day

def run_weekly(job):
    last_job = job.last_job
    print("check weekly run job - len: {0}, data: {1}".format(len(last_job), last_job))
    current_job = job.current_job
    print("check weekly run job - len: {0}, data: {1}".format(len(current_job), current_job))
    for c in range(len(job.idx)):
        print("DEBUG - JOB IS GOING HERE...")
        # if c in [3,4,5]:
        if job.idx[c] in cons.TARGETS:
            print("DEBUG AGAIN - IS JOB GOING HERE??")
            value = current_job[c]
            print("ANOTHER DEBUG", value)
            # print("OLD DATE TYPE: {0}, VALUE: {1}".format(type(oldpaydate), oldpaydate))
            value = value + relativedelta(weeks=+1)
            current_job[c] = value
            # print("IS VALUE CHANGING???", joblist[c])
            job.current_paydate = value
            # print("NEWDATE TYPE: {0}, VALUE: {1}".format(type(newdate), newdate))
        else:
            current_job[c] = current_job[c]
        # print("WHAT DOES JOBLIST LOOK LIKE?>?", joblist)
        current_job[0] = build_summary(job)
        print("OK, WHAT DOES JOBLIST LOOK LIKE, NEW SUMMARY?", current_job)
        job.current_job = current_job
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