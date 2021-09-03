#!/usr/bin/python3

import os
os.system('cd climate && bash ./downloadClimateData.bash')
os.system('cd COVID-19 && python3 covid.py')
os.system('cd travel && python3 travel.py')
os.system('cd climate && python3 climate.py')
os.system('cd vaccine && python3 vaccine.py')
os.system('python3 merge.py')
os.system('mv 2021* ./data')
os.system('python3 merge2.py')
os.system('python3 arizonarun.py')
#os.system('cd climate && rm 2020* && rm F-* && rm sortedClimateDownload.csv')
