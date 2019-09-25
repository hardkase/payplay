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
    client = job["CLIENT"]
    freq = job["FREQUENCY"]
    pay = job["PAY_DATE"]
    summary = "{0} - {1} - {2}".format(client, freq, pay)
    job["SUMMARY"] = summary
    return job

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
    TARGETS = ["PAY_DATE","INPUTS_DUE", "SEND_REPORTS"]
    print(newcols)
    data.columns = newcols
    print(data)
    data = data.apply(lambda x: x.astype(str).str.lower())
    print(data)
    newcolz = ["SUMMARY"]
    for item in newcols:
        newcolz.append(item)
    data = data.reindex(newcolz, axis="columns")
    print(data)
    jobs = []
    for i in range(len(data.index)):
        job = data.iloc[i]
        last_job = job
        if job["FREQUENCY"]=="weekly":
            for a in range(0,52):
                if a < 1:
                    clopy = job
                    for b in range(len(clopy.index)):
                        if clopy.index[b] in TARGETS:
                            value = clopy[b] # This should be a weekday str
                            valist = [number for number, weekday in WEEKDAYS.items() if weekday == value]
                            paywkday = valist.pop()
                            daydiff = (paywkday - datedata[4]) + 7
                            print("CHECK: ", today)
                            firstpay = today + relativedelta(days=+daydiff)
                            print("CHECK2: ", firstpay)
                            clopy[b] = firstpay
                            # IF THIS DOESN@T WORK, try pushing indent  next 3 down past else and left one level
                else:
                    for c in range(len(last_job.index)):
                        clopy = last_job
                        if clopy.index[c] in TARGETS:
                            oldpaydate = clopy[c]
                            newdate = oldpaydate + relativedelta(weeks=+1)
                            clopy[c] = newdate
                    clopy = build_summary(clopy)
                    jobs.append(clopy)
                    last_job = clopy
                clopy = build_summary(clopy)
                jobs.append(clopy)
                last_job = clopy
                # Remaining stuff goes here
        elif "quarterly" in job["FREQUENCY"]:
            pass
        else:
            pass
    final = pd.DataFrame(jobs, columns=newcolz)
    final.to_csv("c:/code/test/tryagain.csv")

if __name__ == '__main__':
    main()
