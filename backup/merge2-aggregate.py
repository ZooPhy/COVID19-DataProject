#!/usr/bin/python3
#from pandas import compat

#compat.PY3 = True


import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta

from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2021, 6, 27)
end_date = date(2021, 8, 10)
for single_date in daterange(start_date, end_date):
	var = single_date.strftime("%Y%m%d")
	current_data = pd.read_csv('./data/' + var + '.csv')
	covid_data = pd.read_csv('./vaccine/'+ var + '-vaccine.csv')
	print(current_data.columns)
	print(covid_data.columns)
	current_data = current_data.merge(covid_data, left_on="fips", right_on='fips')
	print(current_data.columns)
	del current_data['Unnamed: 0_x']
	del current_data['recip_county']
	del current_data['recip_state']
	del current_data['Unnamed: 0_y']
	del current_data['geo_id']
	print(len(current_data.columns))
	current_data.to_csv('./data_with_vaccines/' + var + '.csv')
