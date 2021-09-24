import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta

from datetime import date, timedelta
import os

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_input = raw_input("Enter Start Date (YYYYMMDD):" )
end_input = raw_input("Enter End Date (YYYYMMDD):" )
print(start_input[0:3])
start_date = date(int(start_input[0:4]), int(start_input[4:6]), int(start_input[6:8]))
end_date = date(int(end_input[0:4]), int(end_input[4:6]), int(end_input[6:8]))
for single_date in daterange(start_date, end_date):
	print(single_date)
	printdate = single_date.strftime("%Y%m%d")
	cmd = "cp ./data/" + str(printdate) + ".csv ./newfolder/"
	try:
		os.system(cmd)
	
	except Exception:
		pass
