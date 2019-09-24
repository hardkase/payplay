from __future__ import print_function
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
        self.dflist = []
    def print(self):
        print("Current Data:")
        print("Today's Date: {0}\nYear: {1}\nMonth: {2}\nDay: {3}\nWeekday: {4}\nQuarter: {5}".format(self.today, self.year, self.month, self.day, self.wkday, self.qtr))
        for i in range(len(self.data.index)):
            print(self.data.iloc[i])
        print("Print Complete!")

class Job_Handler(object):
    def __init__(self, job, date_data):
        self.job = job 
        self.first_run = job  # This will be the first processed job of any given jobtype
        self.first_list = []
        self.date_data = date_data
        self.jobtype = job["FREQUENCY"]
        self.jobruns = []
        self.joblists = []
    def reset(self):
        self.__init__()

def main():
    opsys = util.oscheck()
    print(opsys)
    if "Linux" in opsys:
        PATHDATA = con.LINUX_PATHDATA
    else:
        PATHDATA = con.PATHDATA
    alljobs = pd.DataFrame(columns=con.COLUMN_NAMES)
    today = dt.date.today()
    data = util.feed_pandas("{0}{1}{2}".format(PATHDATA[0], PATHDATA[2], PATHDATA[3]))
    print("DEBUG data 0 - create DF: ", data)
    data = util.fix_columns(data)
    print("DEBUG data 1 - normalize columns: ", data)
    data = data.apply(lambda x: x.astype(str).str.lower())
    print("DEBUG data 1 - reduce all str vals to lower: ", data)
    # data = data.insert(0, "SUMMARY", 0)
    data = data.reindex(con.FINAL_COLUMNS, axis=1)
    print("DEBUG data 1 - insert column @ loc[0], add data ", data)
    # truth = data
    dator = Data_Handler(today, data)
    # dator.print()
    # these are DFs
    util.csvmaker(data, "test", PATHDATA)
    alljobs = []
    # adapt loop to focus on qtrly
    # for a in range(len(dator.data.index)):
    for a in range(len(dator.data.index)):
        # job = dator.data.iloc[a]`
        job = dator.data.iloc[a]
        # print("JOB DETAILS: ", job)
        jobject = Job_Handler(job, dator.date_data)
        # print("DEBUG - JOB FREQ: ", jobject.jobtype)
        if jobject.jobtype == "weekly":
            jobject = util.process_weekly(jobject)
        elif "quarterly" in jobject.jobtype:
            jobject = util.process_qtr(jobject)
        else:
            pass
        for item in jobject.jobruns:
            alljobs.append(item)
    final = pd.DataFrame(alljobs, columns=con.FINAL_COLUMNS)
    weekly = final.loc[dator.data['FREQUENCY']=="weekly"]
    monthly = final.loc[dator.data['FREQUENCY']=="monthly"]
    qtrly = final.loc[dator.data['FREQUENCY']=="quarterly"]
    qtrly_aft = final.loc[dator.data["FREQUENCY"]=="quarterly_after"]
    qtr = pd.concat([qtrly, qtrly_aft], ignore_index=True)
    dator.dflist = [weekly, monthly, qtr]
    # print("FINAL INDEX LEN {0}, COL LEN {1}".format(len(final.index), len(final.columns)))
    for item in final.columns:
        print(item)
    # print("INDEX LEN: ", len(final.columns))
    util.csvmaker(final, "shit_series", PATHDATA)
    # print("DEBUG - SERIES - DO WE GET OUTPUT? ", final)
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
