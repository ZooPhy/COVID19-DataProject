# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.bts.gov", None)

import pandas as pd
import numpy as np
from sodapy import Socrata

# Example authenticated client (needed for non-public datasets):
#
# INCLUDE USERNAME AND PASSWORD IN ORDER TO CORRECTLY GENERATE RESULTS
# GENERATE USER AND PASSWORD BY MAKING A SOCRATA ACCOUNT AT THE WEBSITE BELOW
# https://data.bts.gov/Research-and-Statistics/Trips-by-Distance/w96p-f2qv/data
#
# Refer to README for information about generating a unqiue token identifier
client = Socrata("data.bts.gov",
                 "- unique token identifier - ",
                  username="-insert username-",
                password="-insert password-")

# Get results using sodapy
results = client.get("w96p-f2qv", limit=2117622)

# Convert to pandas DataFrame and export as csv
results_df = pd.DataFrame.from_records(results)
results_df.to_csv("travelData.csv",encoding='utf-8')
