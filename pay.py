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
    # a little logic for switching between Linux and Windoze
    opsys = platform.platform()
    print(opsys)
    if "Linux" in opsys:
        PATHDATA = "~/payplay/payplay/fakepay.xlsx"
    else:
        PATHDATA = "c:/code/fakepay.xlsx"
    # Read the xlsx
    data = pd.DataFrame(pd.read_excel(PATHDATA))
    # Date and date data from today
    today = dt.date.today()
    date_data = [today, today.year, today.month, today.day, today.weekday(), pd.Timestamp(today).quarter]
    print(data.columns)
    # Insert the summary column with default data
    data.insert(0, "SUMMARY", "summary here")
    # Change the columns to desired set. You don't need all caps, but do need to get rid of whitespace
    data.columns = cons.final_cols
    print(data)
    # lambda function applied to all data cells - if it's a string, drop to lowercase
    data = data.apply(lambda x: x.astype(str).str.lower())
    print(data)
    # declare and initialize all jobs container before loop logic
    alljobs = []
    # In Pandas, a dataframe has two dimensions - X: Columns and Y: Index (Rows)
    for a in range(len(data.index)):
        # get the row of data
        jobdata = data.iloc[a]
        # Instantiate the job object
        thisjob = Job(jobdata, date_data)
        # Process weekly
        if thisjob.freq == "weekly":
            # Weeklies run 52 times for a year of jobs
            for b in range(0, 52):
                # First iteration needs to be processed
                if b < 1:
                    thisjob = utils.handle_weekly(thisjob)
                    print("how about this :", thisjob.current_paydate)
                else:
                    # The rest of the jobs just need to be moved on a week
                    print("Check job on object, next run: ", thisjob.last_job)
                    thisjob = utils.run_weekly(thisjob)
        elif "quarterly" in thisjob.freq:
            # Quarterly - paid in last month of target quarter
            # Quarterly - after, paid first month of following quarter
            # Use after bool to handle qtr/qtr-aft logic in following functions, rest of functions are same
            after = False
            if thisjob.jobdata["FREQUENCY"].strip() == "quarterly-after":
                after = True
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
        # Some issues getting data direct from object instance, so here I localize it.
        job_runs = thisjob.job_run
        alljobs.extend(job_runs)
    # Pass alljobs into a DataFrame
    final = pd.DataFrame(alljobs, columns = cons.final_cols)
    print("Here We Go! : ", final)
    # Write Dataframe to CSV. Robert's your Father's Brother.
    utils.csvmaker(final, opsys)

if __name__ == '__main__':
    main()

    """
    OK, let's bonk dealing with series, we'll start with a dataframe, split to series for jobs, process all jobs as a list, pass
    lists to alljobs list, take a look -> then see about sending list of jobs back to a DF>GRRRR ARRRGH
    """