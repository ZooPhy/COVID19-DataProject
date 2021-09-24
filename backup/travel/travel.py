# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.bts.gov", None)

import pandas as pd
import numpy as np
from sodapy import Socrata
#Example authenticated client (needed for non-public datasets):
client = Socrata("data.bts.gov",
                 "9gUBYw5E3QOLsHxfn8R51Jfxb",
                  username="masauer2@asu.edu",
                password="MSauer200o!")
print(client.datasets())
# First 2000 results, returned as JSON from API / converted to Python list of
#
#dictionaries by sodapy.
results = client.get("w96p-f2qv",limit="3000000")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.to_csv("travelData.csv",encoding='utf-8')
