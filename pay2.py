# pay2.py 
import pandas as pd
import numpy as np
import datetime as dt 
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import platform
import re



WEEKDAYS = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sundayS"
}

QUARTERS = {
    1: [1, 3],
    2: [4, 6],
    3: [7, 9],
    4: [10, 12]
}

def build_summary(job):
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

def get_current_qtr(date):
    pass

WEEKDAYLIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def main():
    pd.options.mode.chained_assignment = None
    opsys = platform.platform()
    print(opsys)
    if "Linux" in opsys:
        PATHDATA = "~/payplay/payplay/fakepay2.xlsx"
    else:
        PATHDATA = "c:/code/fakepay2.xlsx"
    data = pd.DataFrame(pd.read_excel(PATHDATA))
    today = dt.date.today()
    wkday = today.weekday()
    qtr = pd.Timestamp(today).quarter
    datedata = (today, today.year, today.month, today.day, wkday, qtr)
    # clean
    print(data.columns)
    newcols = ["CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
    final_cols = ["SUMMARY", "CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
    TARGETS = ["PAY_DATE","INPUTS_DUE", "SEND_REPORTS"]
    print(newcols)
    data.columns = newcols
    print(data)
    data = data.apply(lambda x: x.astype(str).str.lower())
    print(data)
    """
    REmove the SUMMAR add...
    newcolz = ["SUMMARY"]
    for item in newcols:
        newcolz.append(item)
    data = data.reindex(newcolz, axis="columns")
    """
    print(data)
    jobs = []
    last_job = []
    for i in range(len(data.index)):
        job = data.iloc[i]
        if job["FREQUENCY"]=="weekly":
            for a in range(0,52):
                joblist = []
                sum1 = "summary"
                clopy = job
                if a < 1:
                    joblist.append(sum1)  # idx 0
                    for b in range(len(clopy.index)):
                        if clopy.index[b] in TARGETS:
                            print("TEST!")
                            value = clopy[b] # This should be a weekday str
                            valist = [number for number, weekday in WEEKDAYS.items() if weekday == value]
                            paywkday = valist.pop()
                            daydiff = (paywkday - datedata[4]) + 7
                            print("CHECK: ", today)
                            firstpay = today + relativedelta(days=+daydiff)
                            print("CHECK2: ", firstpay)
                            joblist.append(firstpay)
                            # IF THIS DOESN@T WORK, try pushing indent  next 3 down past else and left one level
                        else:
                            joblist.append(clopy[b])
                else:
                    current = last_job
                    for c in range(len(current)):
                        if c in [3,4,5]:
                            print("TEST 2!")
                            oldpaydate = current[c]
                            print("OLD DATE TYPE: {0}, VALUE: {1}".format(type(oldpaydate), oldpaydate))
                            newdate = oldpaydate + relativedelta(weeks=+1)
                            print("NEWDATE TYPE: {0}, VALUE: {1}".format(type(newdate), newdate))
                            joblist.append(newdate)
                        else:
                            joblist.append(current[c])
                joblist = build_summary(joblist)
                jobs.append(joblist)
                last_job = joblist
                # Remaining stuff goes here
        elif "quarterly" in job["FREQUENCY"]:
            for a in range(0,4):
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
                
                # Remaining stuff goes here
        else:
            pass
    print("DEBUG - OUTPUT JOBS")
    for item in jobs:
        print("LIST LEN: ", len(item))
        print("LIST: ", item)
    final = pd.DataFrame(jobs, columns=final_cols)
    final.to_csv("c:/code/test/tryagain.csv")

if __name__ == '__main__':
    main()
