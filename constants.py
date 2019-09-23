COLUMN_NAMES = ["CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
TARGETS = ["PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
FINAL_COLUMNS = ["SUMMARY", "CLIENT", "FREQUENCY", "PAY_DATE", "INPUTS_DUE", "SEND_REPORTS"]
PATHDATA = ["c:/code/", "test/", "fakepay", ".xlsx", ".csv"]
LINUX_PATHDATA = ["~/p3_code/payplay/", "test/", "fakepay", ".xlsx", ".csv"]
WEEKDAYLIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
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
default = "NOPE"