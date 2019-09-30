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
    JOB OBJECT - job series and data data
    Read in from initial list, handle per freq
    add summary, copy init processed job to last and push
    initial copy series to all jobs list
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
        # job = data.iloc[i]
        job = Job(data.iloc[i], datedata)
        joblist = job.listify() # testing class function
        for item in joblist:
            print(item)
        newyoke = job.unlist_before(joblist)
        print(newyoke)
        if job.jobdata["FREQUENCY"]=="weekly":
            for a in range(0,52):
                # joblist = cons.TEMPLATE
                # clopy = job
                if a < 1:
                    job = utils.handle_weekly(job)
                    job.current_job = build_sum(job)
                    jobs.append(job.current_job)
                    job.last_job = job.current_job
                    # joblist.clear()
                else:
                    # Something broken in here, appending dates to existing lists or similar...
                    job = utils.run_weekly(job)
                    job.current_job = build_sum(job)
                    jobs.append(job.current_job)
                    job.last_job = job.current_job
                    # current.clear()
                    # Remaining stuff goes here
        elif "quarterly" in job.jobdata["FREQUENCY"]:
            after = False
            if job.jobdata["FREQUENCY"] == "quarterly-after":
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
