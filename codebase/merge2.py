#from pandas import compat

#compat.PY3 = True


import pandas as pd
import numpy as np
import time

timestr = time.strftime("%Y%m%d") + ".csv"

current_data = pd.read_csv('./data/' + timestr)
covid_data = pd.read_csv('./vaccine/data.csv')
print(current_data.columns)
print(covid_data.columns)
current_data = current_data.merge(covid_data, left_on="fips", right_on='fips')
print(len(current_data.columns))
del current_data['Unnamed: 0_x']
del current_data['name']
del current_data['recip_county']
del current_data['recip_state']
del current_data['Unnamed: 0_y']
del current_data['geo_id']
print(len(current_data.columns))
current_data.to_csv('./data_with_vaccines/'+timestr)
