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
Filename: cons.py
Content:
Constants for fake payroll conversion project
"""

WEEKDAYS = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sundayS"
}

QUARTERS = {
    1: [1, 3],
    2: [4, 6],
    3: [7, 9],
    4: [10, 12]
}

WEEKDAYLIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
newcols = ["CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
final_cols = ["SUMMARY", "CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
TARGETS = ["PAY_DATE","INPUTS_DUE", "SEND_REPORTS"]
TEMPLATE = ["summary"]