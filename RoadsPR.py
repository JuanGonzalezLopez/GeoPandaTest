# import geopandas as gpd
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import pygeos
# from shapely.geometry import Polygon,MultiLineString,MultiPolygon
# from scipy.spatial import Delaunay
# from shapely.ops import polygonize, cascaded_union
# import h3pandas
from datetime import datetime


#####################################


ride_data = pd.read_excel('./ride_data/processed_ride_data_dic_24.xlsx')
columns = ride_data.columns.values
for col in columns:

    print(col,ride_data[col].isnull().sum())


zone_data = pd.read_csv('ride_hex_data.csv')

ride_data['Hex_start'] = np.nan
ride_data['Hex_end'] = np.nan
#########################################



def evaluateRow(row):
    id = row['ride_id']
    zone_rows = zone_data.loc[(zone_data['ride_id']==id)]
    if(len(zone_rows)==2):

        start_row = zone_rows.loc[(zone_rows['target']=='start')].reset_index(drop=True)
        start_hex = start_row['Hex_ID'][0]

        end_row = zone_rows.loc[(zone_rows['target']=='end')].reset_index(drop=True)
        end_hex = end_row['Hex_ID'][0]




        row['Hex_start'] = start_hex
        row['Hex_end'] = end_hex

        return row

def mainOperation():


    result = ride_data.apply(evaluateRow,axis=1)
    result.to_csv('Ride_data_with_hex.csv',index=False)
    return result


def datecol(dates):
    mintime = dates.min()
    maxtime = dates.max()

    time = datetime(year=mintime.year,month=mintime.month,day=mintime.day,hour=mintime.hour,minute=0,second=0)
    interval = datetime(minute=5,second=0)
    listdates = []

    while (time <= maxtime):
        if(6<=time.hour<=19):
            time = time +interval
        else:
            time = time + datetime(day=1)
            time.hour = 6
            time.minute = 0

        listdates.append(time)

    return listdates


def prepro(data,target='start'):

    hexes = data['Hex_'+target]

    hexUniq = hexes.unique().reset_index(drop=True)


    dates = data[target+'_time']





if __name__=="__main__":
    mainOperation()

