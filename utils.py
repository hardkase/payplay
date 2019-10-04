# utils
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import cons
import re

def handle_weekly(job):
    job.job_run[:] = []
    job.last_job[:] = []
    first_job = job.jobdata
    current_job = []
    for b in range(len(job.idx)):        
        if job.idx[b] in cons.TARGETS:
            value = first_job[b].strip()
            target_day = get_wkday_val(value)
            daydiff = (target_day - job.weekday) + 7
            firstday = job.today + relativedelta(days=+daydiff)
            current_job.append(firstday)
            job.current_paydate = firstday
            #Trying to not do else because nothing should change
        else:
            current_job.append(first_job[b])
        current_job[0] = build_summary(job)
        job.last_job = current_job
        job.job_run.append(current_job)
        print("Another bloody check - current job should be good", current_job)
    return job

def run_weekly(job):
    last_job = job.last_job
    current_job = []
    for c in range(len(job.idx)):
        if job.idx[c] in cons.TARGETS:
            value = last_job[c]
            value = value + relativedelta(weeks=+1)
            current_job.append(value)
            job.current_paydate = value
        else:
            current_job.append(last_job[c])
        current_job[0] = build_summary(job)
        print("OK, WHAT DOES JOBLIST LOOK LIKE, NEW SUMMARY?", current_job)
        job.last_job = current_job
        job.job_run.append(current_job)
        print(job.last_job)
    return job

def handle_qtr(job, after):
    job.job_run[:] = []
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
            value = weekend_checker(value)
            # paydate = datebuilder(job_data[0], qtr_data[get_qtr_month], value)
            current_job.append(value)
            job.current_paydate = value
        else:
            current_job.append(first_job[a])
            # DEBUG shows jumping from iteration 1 to build summary, so logic funky somwehre here
    current_job[0] = build_summary(job)
    job.last_job = current_job
    job.job_run.append(current_job)  # might need to switch append/extend...
    print("Another bloody check - current job should be good", job.last_job)
    return job

def run_qtr_jobs(job):
    last_gig = job.last_job
    current_job = []
    for i in range(len(job.idx)):
        if job.idx[i] in cons.TARGETS:
            new_date = last_gig[i] + relativedelta(months=+3)
            new_date = weekend_checker(new_date)
            current_job.append(new_date)
            job.current_paydate = new_date
        else:
            current_job.append(last_gig[i])
    current_job[0] = build_summary(job)
    job.last_job = current_job
    job.job_run.append(current_job)
    print("Another bloody check - current job should be good", current_job)
    return job

def handle_monthly(job):
    job.job_run[:] = []
    first_job = job.jobdata
    current_job = []
    job_data = [job.year, job.month]
    for x in range(len(job.idx)):
        if job.idx[x] in cons.TARGETS:
            value = first_job[x]
            value = value_checker(value, job_data)
            # paydate = datebuilder(job_data[0], job_data[1], value)
            value = weekend_checker(value)
            current_job.append(value)
            job.current_paydate = value
        else:
            current_job.append(first_job[x])
    current_job[0] = build_summary(job)
    job.last_job = current_job
    job.job_run.append(current_job)
    return job

def run_monthly(job):
    last_gig = job.last_job
    current_job = []
    print("TEST - is last job right?: ", current_job) # tweak and replace
    for i in range(len(job.idx)):
        if job.idx[i] in cons.TARGETS:
            print("Test we're getting here")
            print("old date", last_gig[i])
            new_date = last_gig[i] + relativedelta(months=+1)
            print("CHECK: first job len {0}, first_job: {1}".format(len(job.first_job), job.first_job))
            og_pay_value = job.jobdata[i]
            job_data = [new_date.year, new_date.month]
            new_date = value_checker(og_pay_value, job_data)
            new_date = weekend_checker(new_date)
            print("new date", new_date)
            current_job.append(new_date)
            job.current_paydate = new_date
        else:
            current_job.append(last_gig[i])
    current_job[0] = build_summary(job)
    job.last_job = current_job
    job.job_run.append(current_job)
    print("Another bloody check - current job should be good", current_job)
    return job

def csvmaker(data, opsys):
    if "Linux" in opsys:
        path = "~/payplay/payplay/final_output.csv"
    else:
        path = "c:/code/final_output.csv"
    data.to_csv(path)

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
        print("culprits: a {0} b {1} c{2}".format(year, month, day))
        error = True
    except TypeError as er2:
        print("Type Error: ", er2)
        error = True
    if error:
        print("************it's not working!!!****************")
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
    last_day = "dude..."
    if numero:
        last_day = value
    elif stringer:
        cloaked_int = value.isdigit()
        if cloaked_int:
            print(value, type(value))
            last_day = int(value)
        if stringer and value == "lwd":
            last_day = get_lwd(job_data[0], job_data[1])
        elif stringer and "-" in value:
            last_day = get_lwd(job_data[0], job_data[1])
            modifier = value_splitter(value)
            print("Value checker check-last: {0}, mod: {1}".format(last_day, modifier))
            last_day = last_day - modifier
    else:
        last_day = 0
    date = datebuilder(job_data[0], job_data[1], last_day)
    return date

def value_splitter(value):
    value = re.split("-", value)
    modifier = int(value[1].strip())
    return modifier

def weekend_checker(date):
    wkend = False
    wkday = date.weekday()
    if wkday in [5, 6]:
        wkend = True
    if wkend and wkday == 6:
        date = date + relativedelta(days=-2)
    elif wkend and wkday == 5:
        date = date + relativedelta(days=-1)
    return date

def get_wkday_val(value):
    valist = [number for number, weekday in cons.WEEKDAYS.items() if weekday == value]
    target_day = valist.pop()
    return target_day

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