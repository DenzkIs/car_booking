import datetime
print(datetime.datetime.isoweekday(datetime.datetime.now()))
print(datetime.datetime.isocalendar(datetime.datetime.now() + datetime.timedelta(days=0)).week)

td = datetime.date(2023, 12, 31) - datetime.date.today()
print(td)
print(datetime.date(2023, 12, 31) - (datetime.date(2023, 1, 1)))
print(datetime.datetime.isocalendar(datetime.date.today()).week)
