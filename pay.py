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
        PATHDATA = "~/payplay/payplay/fakepay2.xlsx"
    else:
        PATHDATA = "c:/code/fakepay2.xlsx"
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
    lastjob = pd.Series(cons.final_cols, index=cons.final_cols)
    for a in range(len(data.index)):
        jobdata = data.iloc[a]
        thisjob = Job(jobdata, date_data)
        print(thisjob.jobdata)
        print(thisjob.client)
        if thisjob.freq == "weekly":
            for b in range(0, 52):
                if b < 1:
                    thisjob = utils.handle_weekly(thisjob)
                else:
                    thisjob = utils.run_weekly(thisjob)
        elif "quarterly" in thisjob.freq:
            for b in range(0, 4):
                if b < 1:
                    pass
                else:
                    pass
        else:  #MONTHLY
            for b in range(0, 12):
                if b < 1:
                    pass
                else:
                    pass
        alljobs.append(thisjob.current_job)
    for item in alljobs:\
        print("Debug - type: {0}, data: {1}".format(type(item), item))

if __name__ == '__main__':
    main()

    """
    OK, let's bonk dealing with series, we'll start with a dataframe, split to series for jobs, process all jobs as a list, pass
    lists to alljobs list, take a look -> then see about sending list of jobs back to a DF>GRRRR ARRRGH
    """