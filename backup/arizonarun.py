import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import timedelta

from datetime import date, timedelta

var = datetime.today()
var = var - timedelta(days = 0)
timestr = var.strftime('%Y%m%d') + '.csv'
df = pd.read_csv("./data_with_vaccines/" + timestr)
df.columns = df.columns.str.strip().str.lower()
df = df.loc[df['state'] == "AZ"]
df1 = df[['admin2','state','fips','cases','deaths','tempmedian','tempmean','prcpmedian','prcpmean','population','pop_density','administered_dose1_pop_pct','administered_dose1_recip','administered_dose1_recip_12plus','administered_dose1_recip_12pluspop_pct','administered_dose1_recip_18plus','administered_dose1_recip_18pluspop_pct','administered_dose1_recip_65plus','administered_dose1_recip_65pluspop_pct','completeness_pct','mmwr_week','series_complete_12plus','series_complete_12pluspop','series_complete_12pluspop_pct_svi','series_complete_18plus','series_complete_18pluspop','series_complete_18pluspop_pct_svi','series_complete_65plus','series_complete_65pluspop','series_complete_65pluspop_pct_svi','series_complete_pop_pct','series_complete_pop_pct_svi','series_complete_yes','svi_ctgy']]
df1.to_csv("./az_data/" + timestr)
