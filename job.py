
import pandas as pd 
import numpy as np 
import datetime as dt
import utils
import cons


class Job(object):
    def __init__(self, jobdata, date_data): # job: series, today's datedataclient, frequency, paydate, inputs, reports, 
        self.jobdata = jobdata
        self.date_data = date_data
        self.today = date_data[0]
        self.year = date_data[1]
        self.month = date_data[2]
        self.day = date_data[3]
        self.weekday = date_data[4]
        self.qtr = date_data[5]
        self.summary = "summary"
        self.client = jobdata["CLIENT"]
        self.freq = jobdata["FREQUENCY"]
        self.paydate = jobdata["PAY_DATE"]
        self.inputs = jobdata["INPUTS_DUE"]
        self.reports = jobdata["SEND_REPORTS"]
        self.joblist = []
        self.current_job = []
        self.last_job = []
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