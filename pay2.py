# pay2.py 
import pandas as pd
import numpy as np
import datetime as dt 
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import platform
import re
import utils
import cons


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
    data.columns = cons.newcols
    print(data)
    data = data.apply(lambda x: x.astype(str).str.lower())
    print(data)
    jobs = []
    last_job = []
    for i in range(len(data.index)):
        job = data.iloc[i]
        if job["FREQUENCY"]=="weekly":
            for a in range(0,52):
                joblist = cons.TEMPLATE
                clopy = job
                if a < 1:
                    for b in range(len(clopy.index)):
                        if clopy.index[b] in cons.TARGETS:
                            print("TEST!")
                            value = clopy[b] # This should be a weekday str
                            valist = [number for number, weekday in cons.WEEKDAYS.items() if weekday == value]
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
                joblist = utils.build_summary(joblist)
                jobs.append(joblist)
                last_job = joblist
                # Remaining stuff goes here
        elif "quarterly" in job["FREQUENCY"]:
            after = False
            if job["FREQUENCY"] == "quarterly-after":
                after = True
            for a in range(0,4):
                push = a
                if push < 1:
                    joblist = utils.handle_qtr(job, datedata, after)
                    initial_run = joblist
                else:
                    joblist = utils.run_qtr_jobs(initial_run, push)
                jobs.append(joblist)
                # Remaining stuff goes here
        else:
            pass
    print("DEBUG - OUTPUT JOBS")
    for item in jobs:
        print("LIST LEN: ", len(item))
        print("LIST: ", item)
    final = pd.DataFrame(jobs, columns=cons.final_cols)
    final.to_csv("c:/code/test/tryagain.csv")

if __name__ == '__main__':
    main()
