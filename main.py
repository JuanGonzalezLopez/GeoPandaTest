import pandas as pd
from GridSystem import PuertoRicoGISCode
import geopandas as gpd
from RoadsPR import HexagonData
from Preprocessing import datecolumns
from redesigned import grouping
from ClusterTest import Clusters
from solapado import overlap
import gc


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
    print("Loading files...")
    # Step 1
    filename = './Data/processed_ride_data_dic_24.xlsx'
    data = pd.read_excel(filename)
    puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
    roads = gpd.read_file(r'PRRoads/hotosm_pri_roads_lines.shp')
    # Step 2
    print("Creating Hexagonal Grid...")
    print("Ignore warnings...")
    GeoPR = PuertoRicoGISCode(puertorico,roads,index=49)
    HexZones = GeoPR.ZoneIndicator(reso=10,show=True,data=data)
    # Step 3


    print("Assigning zones to all rides...")
    NewData = HexagonData(data=data, zone=HexZones)
    NewDataDF = NewData.mainOperation(output='./Output/Ride_data_with_hex.csv')


    # Garbage collecting unused variables
    del HexZones
    del GeoPR
    del puertorico
    del roads

    gc.collect()
    # Step 4

    print("Create time interval")
    # dates = datecolumns(step_interval=5) # 5 minutes
    dates = datecolumns(data=NewDataDF,step_interval=5) # 5 minutes
    datesDF = dates.intervalize()


    # Step 4b
    print("Adding Clusters")
    cluster = Clusters(datesDF,12)
    dataClu= cluster.createCluster()


    # Step 5
    print("Transforming data aggregation...")
    prefinalized = grouping(parent=True,data=dataClu)
    grData = prefinalized.returnDF()


    solapado = overlap(grData)
    finalized= solapado.returnDF()

    # TODO Dummies
    print("...Done")
    return finalized

if __name__=="__main__":
    main()




