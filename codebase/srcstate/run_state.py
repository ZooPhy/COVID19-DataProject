#!/usr/bin/python3

import os
#os.system('cd climate_state && bash ./downloadClimateData.bash')
os.system('cd covid_state && python covid_state.py')
#os.system('cd travel_state && python travel_state.py')
os.system('cd climate_state && python climate_state.py')
os.system('python merge_state.py')
os.system('mv 2021* ./data')
os.system('cd climate_state && rm 2020* && rm F-* && rm sortedClimateDownload.csv')
