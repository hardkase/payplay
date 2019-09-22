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
        # self.qtr = get_quarter(today)
    def print(self):
        print("Current Data:")
        print("Today's Date: {0}\nYear: {1}\nMonth: {2}\nDay: {3}\nWeekday: {4}".format(self.today, self.year, self.month, self.day, self.wkday))
        for i in range(len(self.data.index)):
            print(self.data.iloc[i])
        print("Print Complete!")

def main():
    today = dt.date.today()
    data = pd.DataFrame(pd.read_excel("c:/code/fakepay.xlsx"))
    dator = Data_Handler(today, data)
    data = util.fix_columns(dator.data)
    data = util.insert_column(dator.data, 0, "SUMMARY", "Summary Goes Here")
    data = util.to_lower(dator.data) # This isn't working ...
    dator.data = data
    dator.print()
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
