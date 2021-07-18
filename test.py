from datetime import datetime, date
import datetime as dt

days = dt.date.weekday(dt.datetime.strptime("2021/06/21","%Y/%m/%d"))

print(days)