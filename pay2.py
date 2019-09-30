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
from job import Job

WEEKDAYLIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def main():
    """"
    RE: Weekly
    If today is Tuesday and payday is Friday
    1) Tuesday = 1, Friday = 4
    We need to advance the date by 3
    2) If today is Friday and payday is Tuesday
    We need to decrement date by 3
    1) current day 1 - target date  4 = -3 but -(-3) is + 3 so...
    1) target day 4 - current date 1 = 3
    2) current day 4 - target date = 3
    2) target day 1 - target date 4 = -3
    if relativedelta is days=+ want second option
    if reltivedelta is days=- want first option
    I think this is commutative so either option works
    provided correct operator is used
    +7 brings target date to next week so gtg
    """
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
        jobbo = Job(data.iloc[i], datedata)
        joblist = jobbo.listify() # testing class function
        for item in joblist:
            print(item)
        newyoke = jobbo.unlist_before(joblist)
        print(newyoke)
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
                        else:
                            joblist.append(clopy[b])
                    jobs.append(joblist)
                    last_job = joblist
                    # joblist.clear()
                else:
                    # Something broken in here, appending dates to existing lists or similar...
                    current = []
                    current = cons.TEMPLATE
                    for c in range(len(current)):
                        if c in [3,4,5]:
                            print("TEST 2!")
                            oldpaydate = last_job[c]
                            print("OLD DATE TYPE: {0}, VALUE: {1}".format(type(oldpaydate), oldpaydate))
                            newdate = oldpaydate + relativedelta(weeks=+1)
                            print("NEWDATE TYPE: {0}, VALUE: {1}".format(type(newdate), newdate))
                            current[c] = newdate
                        else:
                            current[c] = last_job[c]
                        current = utils.build_summary(current)
                        jobs.append(current)
                        last_job = current
                        # current.clear()
                # Remaining stuff goes here
        elif "quarterly" in job["FREQUENCY"]:
            after = False
            if job["FREQUENCY"] == "quarterly-after":
                after = True
            for a in range(0,4):
                push = a
                if push < 1:
                    joblist = utils.handle_qtr(job, datedata, after)
                    jobs.append(joblist)
                    last_job = joblist
                    print("DEBUG QTR - LIST: ", last_job)
                    # joblist.clear()
                else:

                    joblist = utils.run_qtr_jobs(last_job, push)
                    jobs.append(joblist)
                    last_job = joblist
                    # joblist = []
                # Remaining stuff goes here
        else:
            pass
    print("DEBUG - OUTPUT JOBS")
    for item in jobs:
        print("LIST LEN: ", len(item))
        print("LIST: ", item)
    final = pd.DataFrame(jobs, columns=cons.final_cols)
    # final = final.transpose()
    final.columns = cons.final_cols
    final.to_csv("c:/code/test/tryagain.csv")

if __name__ == '__main__':
    main()
