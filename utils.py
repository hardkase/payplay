# utils
import datetime as dt
from dateutil.relativedelta import relativedelta
import cons

def handle_qtr(job, datedata, after):
    qtr = datedata[5]
    get_qtr_month = 1
    if after:
        qtr = qtr + 1
        if qtr > 4:
            qtr = qtr - 4
        get_qtr_month = 0
    qtr_data = get_qtr(qtr)
    joblist = cons.TEMPLATE
    for a in range(len(job.index)):
        if job.index[a] in cons.TARGETS:
            value = job[a]
            string = strcheck(value)
            numero = intcheck(value)
            if string:
                value = value.strip()
                hoax = hiding_number(value)
                if hoax:
                    value = scoop_num(value)
            if string and "lwd" in value:
                payday = get_lwd(datedata[1], qtr_data[get_qtr_month])
                if "-" in value:
                    value = re.sub(" ", "", value)
                    value = value.strip()
                    value = re.split("-", value)
                    modifier = value[1]
                    payday = payday + relativedelta(day=-modifier)
            paydate = datebuilder(datedata[1], qtr_data[get_qtr_month], payday)
            joblist.append(paydate)
    print(joblist)
    return joblist

def run_qtr_jobs(job, push):
    modifier = push * 3
    for i in range(len(job)):
        if i in [3,4,5]:
            job[i] = job[i] + relativedelta(month=+modifier)
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
        newdate = dt.date(year, month, date)
    except ValueError as er1:
        print("Value Error: ", er1)
        error = True
    except TypeError as er2:
        print("Type Error: ", er2)
        error = True
    if error:
        newdate = dt.date(1941, 12, 7)
    return newdate

"""
or a in range(0,4):
                joblist = []
                sum1 = "summary"
                clopy = job
                if clopy["FREQUENCY"].strip() == "quarterly":
                    if a < 1:
                        qtr = datedata[5]
                        qtr_data = get_qtr(qtr)
                        print("QTR: {0}".format(qtr))
                        joblist.append(sum1)  # idx 0
                        for b in range(len(clopy.index)):
                            if clopy.index[b] in TARGETS:
                                print("TEST!")
                                value = clopy[b] # This will be a day of the month or lwd etc
                                if isinstance(value, str):
                                    lwd = get_lwd(datedata[1], qtr_data[1])
                                    newdate = dt.date(datedata[1], qtr_data[1], lwd)
                                    if value.strip() == "lwd":
                                        joblist.append(newdate)
                                    elif re.match(r"lwd-[0-9]", value): 
                                        modifier = re.split("-", value)
                                        newdate = newdate + relativedelta(days=-modifier[1])
                                        joblist.append(newdate)
                                elif isinstance(value, int):
                                    newdate = dt.date(datedata[1], qtr_data[1], value)
                                    joblist.append(newdate)
                            else:
                                joblist.append(clopy[b])
                        joblist = build_summary(joblist)
                        jobs.append(joblist)
                        last_job = joblist
                    else:
                        current = last_job
                        for c in range(len(current)):
                            if c in [3,4,5]:
                                print("TEST 2!")
                                oldpaydate = current[c]
                                print("OLD DATE TYPE: {0}, VALUE: {1}".format(type(oldpaydate), oldpaydate))
                                newdate = oldpaydate + relativedelta(months=+3)
                                print("NEWDATE TYPE: {0}, VALUE: {1}".format(type(newdate), newdate))
                                joblist.append(newdate)
                            else:
                                joblist.append(current[c])
                    joblist = build_summary(joblist)
                    jobs.append(joblist)
                    last_job = joblist
                else:
                    if a < 1:
                        qtr = datedata[5]
                        qtr = qtr + 1
                        if qtr > 4:
                            qtr = qtr - 4
                        qtr_data = get_qtr(qtr)
                        print("QTR: {0}".format(qtr))
                        joblist.append(sum1)  # idx 0
                        for b in range(len(clopy.index)):
                            if clopy.index[b] in TARGETS:
                                print("TEST!")
                                value = clopy[b] # This will be a day of the month or lwd etc
                                if isinstance(value, int):
                                    newdate = dt.date(datedata[1], qtr_data[0], value)
                                    joblist.append(newdate)
                                elif isinstance(value, str):
                                    lwd = get_lwd(datedata[1], qtr_data[0])
                                    newdate = dt.date(datedata[1], qtr_data[0], lwd)
                                    if value.strip() == "lwd":
                                        joblist.append(newdate)
                                    elif re.match(r"lwd-[0-9]", value): 
                                        print("DATE VALUE:  {0}, TYPE: {1}".format(value, type(value)))
                                        modifier = re.split("-", value)
                                        print("DEBUG", modifier)
                                        newdate = newdate + relativedelta(days=-modifier[1])
                                        joblist.append(newdate)
                            else:
                                joblist.append(clopy[b])
                        joblist = build_summary(joblist)
                        jobs.append(joblist)
                        last_job = joblist
                    else:
                        current = last_job
                        for c in range(len(current)):
                            if c in [3,4,5]:
                                print("TEST 2!")
                                oldpaydate = current[c]
                                print("OLD DATE TYPE: {0}, VALUE: {1}".format(type(oldpaydate), oldpaydate))
                                newdate = oldpaydate + relativedelta(months=+3)
                                print("NEWDATE TYPE: {0}, VALUE: {1}".format(type(newdate), newdate))
                                joblist.append(newdate)
                            else:
                                joblist.append(current[c])
                        joblist = build_summary(joblist)
                        jobs.append(joblist)
                        last_job = joblist
"""
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
    qtr_data = QUARTERS.get(qtr)
    return qtr_data

