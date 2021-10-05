import pandas as pd

import numpy as np


data = pd.read_csv('Ride_data_with_hex.csv')


print(data[(data['Hex_start'].isin(['hexa_287','hexa_284','hexa_418','hexa_393','hexa_138','hexa_334','hexa_125']) |

            data['Hex_end'].isin(['hexa_287','hexa_284','hexa_418','hexa_393','hexa_138','hexa_334','hexa_125']
                                 ))])





# period = pd.Period(df['dt'][0]).day_of_year
# step_interval = 5/60
#
# minimum_hour = int(data['start_time_scalar'].min())
# maximum_hour = int(data['end_time_scalar'].max())
#
# unique_time = np.arange(minimum_hour,maximum_hour,step_interval)
# hour = 1.0
# limit = int(60/5)
#
# for i in range(0, len(unique_time) - limit):
#
#     smallest = unique_time[i]
#     largest = smallest + hour
#
#
#     if (smallest.is_integer()):
#
#         unique_time[i+limit] = largest
#
# unique_time