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
class HexagonData():
    def __init__(self,filename= './ride_data/processed_ride_data_dic_24.xlsx',data=None):
        if(data!=None):
            self.ride_data = data
        else:
            self.ride_data = pd.read_excel(filename)

        columns = self.ride_data.columns.values
        for col in columns:

            print(col,self.ride_data[col].isnull().sum())


        self.zone_data = pd.read_csv('ride_hex_data.csv')

        self.ride_data['Hex_start'] = np.nan
        self.ride_data['Hex_end'] = np.nan
#########################################



    def evaluateRow(self,row):
        id = row['ride_id']
        zone_rows = self.zone_data.loc[(self.zone_data['ride_id']==id)]
        if(len(zone_rows)==2):

            start_row = zone_rows.loc[(zone_rows['target']=='start')].reset_index(drop=True)
            start_hex = start_row['Hex_ID'][0]

            end_row = zone_rows.loc[(zone_rows['target']=='end')].reset_index(drop=True)
            end_hex = end_row['Hex_ID'][0]




            row['Hex_start'] = start_hex
            row['Hex_end'] = end_hex

            return row

    def mainOperation(self,output='Ride_data_with_hex.csv'):


        result = self.ride_data.apply(self.evaluateRow,axis=1)
        result.to_csv(output,index=False)
        return result




if __name__=="__main__":
    temp = HexagonData()
    temp.mainOperation()

