import pandas as pd


def createHullData():
    df = pd.read_excel('./ride_data/processed_ride_data_dic_24.xlsx')
    hull = df[['start_lat', 'start_long']]
    hull = hull[hull['start_lat'] >= 17].reset_index(drop=True)
    hull = hull.rename(columns={"start_lat": "Latitude", "start_lon": "Longitude"})
    return hull

hull = createHullData()

# df = pd.read_excel('./ride_data/processed_ride_data_dic_24.xlsx')
