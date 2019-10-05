"""
Project: PayPlay - mock payroll data conversion exercise
Description:
1.) Read in XLSX of payroll jobs using Pandas
2.) Sanitize data (alter columns, drop strings to lower, etc)
3.) Split each data row into a job
4.) Process jobs as required by job 'Frequency'
5.) Pass processed jobs 'Job Run' into a container
6.) Pass job runs into all jobs container
7.) Pass all jobs list into a new Pandas DataFrame
8.) Output Dataframe to CSV
Author: Patrick Collins
Filename: pay.py
Content:
Main function for project
"""
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

def main():
    opsys = platform.platform()
    print(opsys)
    if "Linux" in opsys:
        PATHDATA = "~/payplay/payplay/fakepay.xlsx"
    else:
        PATHDATA = "c:/code/fakepay.xlsx"
    data = pd.DataFrame(pd.read_excel(PATHDATA))
    today = dt.date.today()
    date_data = [today, today.year, today.month, today.day, today.weekday(), pd.Timestamp(today).quarter]
    print(data.columns)
    data.insert(0, "SUMMARY", "summary here")
    data.columns = cons.final_cols
    print(data)
    data = data.apply(lambda x: x.astype(str).str.lower())
    print(data)
    alljobs = []
    for a in range(len(data.index)):
        jobdata = data.iloc[a]
        thisjob = Job(jobdata, date_data)
        print("JOB DATA: ", thisjob.jobdata)
        print("DATA INDEX: ", thisjob.idx)
        print("Client: ", thisjob.client)
        if thisjob.freq == "weekly":
            for b in range(0, 52):
                if b < 1:
                    thisjob = utils.handle_weekly(thisjob)
                    print("how about this :", thisjob.current_paydate)
                else:
                    print("Check job on object, next run: ", thisjob.last_job)
                    thisjob = utils.run_weekly(thisjob)
        elif "quarterly" in thisjob.freq:
            after = False
            if thisjob.jobdata["FREQUENCY"].strip() == "quarterly-after":
                after = True
                for b in range(0, 4):
                    if b < 1:
                        thisjob = utils.handle_qtr(thisjob, after)
                    else:
                        thisjob = utils.run_qtr_jobs(thisjob)
            else:
                for b in range(0, 4):
                    if b < 1:
                        thisjob = utils.handle_qtr(thisjob, after)
                    else:
                        thisjob = utils.run_qtr_jobs(thisjob)
        else:  #MONTHLY
            for b in range(0, 12):
                if b < 1:
                    utils.handle_monthly(thisjob)
                else:
                    utils.run_monthly(thisjob)
        job_runs = thisjob.job_run
        alljobs.extend(job_runs)
    for item in alljobs:
        print("TEST! ", item)     
    print("LEN OF ALL JOBS: ", len(alljobs))  
    final = pd.DataFrame(alljobs, columns = cons.final_cols)
    print("Here We Go! : ", final)
    utils.csvmaker(final, opsys)

if __name__ == '__main__':
    main()

    """
    OK, let's bonk dealing with series, we'll start with a dataframe, split to series for jobs, process all jobs as a list, pass
    lists to alljobs list, take a look -> then see about sending list of jobs back to a DF>GRRRR ARRRGH
    """