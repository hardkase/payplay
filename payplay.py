import pandas as pd 
import numpy as np 
import datetime as dt 
import constants as con 
import utilities as util

class Data_Handler(object):
    def __init__(self, today, data):
        self.today = today
        self.data = data
        self.year = today.year
        self.month = today.month
        self.day = today.day
        self.wkday = today.weekday()
        self.qtr = pd.Timestamp(today).quarter
        self.date_data = [self.today, self.year, self.month, self.day, self.wkday, self.qtr]
    def print(self):
        print("Current Data:")
        print("Today's Date: {0}\nYear: {1}\nMonth: {2}\nDay: {3}\nWeekday: {4}\nQuarter: {5}".format(self.today, self.year, self.month, self.day, self.wkday, self.qtr))
        for i in range(len(self.data.index)):
            print(self.data.iloc[i])
        print("Print Complete!")

class Job_Handler(object):
    # experiment extending data object
    def __init__(self, job, date_data):
        self.job = job 
        self.first_run = job  # This will be the first processed job of any given jobtype
        self.date_data = date_data
        # self.truth = tru
        self.jobtype = job["FREQUENCY"]
        self.jobrun = []
    def reset(self):
        self.__init__()

def main():
    alljobs = pd.DataFrame(columns=con.COLUMN_NAMES)
    today = dt.date.today()
    data = pd.DataFrame(pd.read_excel("{0}{1}{2}".format(con.PATHDATA[0], con.PATHDATA[2], con.PATHDATA[3])))
    # dator = Data_Handler(today, data)
    data = util.fix_columns(data)
    data.data = util.insert_column(data, 0, "SUMMARY", "Summary Goes Here")
    data = util.to_lower(data)
    truth = data
    dator = Data_Handler(today, data)
    dator.print()
    # weekly = dator.data["FREQUENCY"] ==("weekly")
    weekly = dator.data.loc[dator.data['FREQUENCY']=="weekly"]
    monthly = dator.data.loc[dator.data['FREQUENCY']=="monthly"]
    qtrly = dator.data.loc[dator.data['FREQUENCY']=="quarterly"]
    qtrly_aft = dator.data.loc[dator.data['FREQUENCY']=="quarterly-after"]
    print("DEBUG - WEEKLY:\n", weekly)
    print("DEBUG - MONTHLY:\n", monthly)
    print("DEBUG - QUARTERLY:\n", qtrly)
    print("DEBUG - QUARTERLY-AFTER:\n", qtrly_aft)
    util.csvmaker(data, "test")
    alljobs = []
    for a in range(len(dator.data.index)):
        job = dator.data.iloc[a]
        print("JOB DETAILS: ", job)
        jobject = Job_Handler(job, dator.date_data)
        print("DEBUG - JOB FREQ: ", jobject.jobtype)
        if jobject.jobtype == "weekly":
            jobject = util.process_weekly(jobject)
        elif jobject.jobtype == "quarterly":
            pass
            # jobject = util.process_qtr(jobject)
        elif jobject.jobtype == "quarterly-after":
            pass
            # jobject = util.process_qtr_aft(jobject)
        else:
            pass
        for item in jobject.jobrun:
            print("JOB INDEX: ", len(item.index))
        alljobs.append(jobject.jobrun)
    for item in alljobs:
        print("DEBUG: ", item)
    final = pd.DataFrame([jobject.jobrun])
    print("DEBUG - DO WE GET OUTPUT? ", final)
            # jobject = util.process_monthly(jobject)
        # print("DEBUG - JOBJECT", job.jobtype)
    # jobject = JobHandler(dator)
    # for i in range(len())
    # This is all working, ready to start processing each job type...
if __name__ == '__main__':
    main()

"""
# create script object
# keep main clean, offshore functions to utils
# break up clunky functions into smaller functions
# push reused vars out to constants
# change column names
# drop all string content to lower()
# add a summary column
# sort by freq type
# export results to csv as truth
# based on freq type, generate jobs
# push results out to csv
"""
