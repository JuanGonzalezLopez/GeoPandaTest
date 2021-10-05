import pandas as pd
from GridSystem import PuertoRicoGISCode
import geopandas as gpd
from RoadsPR import HexagonData
from Preprocessing import datecolumns
from redesigned import grouping


def main():
    """
    Step 1:
        Import the data | Shapefiles (cities, roads)
    Step 2:
        Run the Hexagon grid zone (PuertoRicoGISCode.ZoneIndicator())
    Step 3:
        Assign zones to each ride with the Hexagon Grid Zone data (HexagonData.mainOperation())
    Step 4:
        Assign interval label to a timeframe (datecolumns.intervalize())
    Step 5:
        Add all rides between a set amount of time inside intervals (grouping())

    :return:
    """

    # Step 1
    filename = './Data/processed_ride_data_dic_24.xlsx'
    data = pd.read_excel(filename)
    puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
    roads = gpd.read_file(r'PRRoads/hotosm_pri_roads_lines.shp')
    # Step 2
    GeoPR = PuertoRicoGISCode(puertorico,roads)
    HexZones = GeoPR.ZoneIndicator(reso=10,show=False,data=data)
    # Step 3
    NewData = HexagonData(data=HexZones)
    NewDataDF = NewData.mainOperation(output='./Output/Ride_data_with_hex.csv')
    # Step 4
    dates = datecolumns(data=NewDataDF,step_interval=5) # 5 minutes
    datesDF = dates.intervalize()
    # Step 5
    prefinalized = grouping(datesDF)

    # TODO Final interval DF (horas solapadas)

    return prefinalized

if __name__=="__main__":
    main()




