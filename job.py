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
Filename: job.py
Content:
Job Class - ad hoc container for job and date data
"""

import pandas as pd 
import numpy as np 
import datetime as dt
import utils
import cons


class Job(object):
    """
    After some frustration dealing with Series when processing jobs, decided to give creating a job object a try.
    Considerably easier to deal with. Contains job data (series), and parsed out date data. Parses reused job details, the 
    jobdata index, the first run, the last job, and a list of all the jobs created for a particular job. Includes functions
    to create a list from a series, and two unused functions to create a series from a list.
    """
    def __init__(self, jobdata, date_data): # job: series, today's datedataclient, frequency, paydate, inputs, reports, 
        self.jobdata = jobdata
        self.date_data = date_data
        self.today = date_data[0]
        self.year = date_data[1]
        self.month = date_data[2]
        self.day = date_data[3]
        self.weekday = date_data[4]
        self.qtr = date_data[5]
        self.current_paydate = ""  # For test purposes only, remove later
        self.client = jobdata["CLIENT"]
        self.freq = jobdata["FREQUENCY"]
        self.paydate = jobdata["PAY_DATE"]
        self.inputs = jobdata["INPUTS_DUE"]
        self.reports = jobdata["SEND_REPORTS"]
        # back to lists cuz series aint playin, convert back to DF at end
        self.idx = self.jobdata.index  # Column values of jobdata Series
        self.first_job = [] # Very first 'handle' job
        self.last_job = [] # last completed job
        self.job_run = [] # this will be a list of jobs, all of same freq type
    def listify(self):
        itemlist = []
        for entry in self.jobdata:
            itemlist.append(entry)
        return itemlist
    def unlist_before(self, somelist):
        newseries = pd.Series(somelist, index=cons.newcols)
        return newseries
    def unlist_after(self, somelist):
        newseries = pd.Series(somelist, columns=cons.final_cols)
        return newseries