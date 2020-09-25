from datetime import datetime
now = datetime.now()
day = now.strftime("%d")
yesterday = int(day) - 1
print(day)
print(type(yesterday))