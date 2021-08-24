import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Polygon


class ShapeFileExp():
    def __init__(self):
        self.shapefile = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
        # self.shapefile = gpd.read_file(r'PRRoads/hotosm_pri_roads_lines.shp')

    def showAllColumns(self):
        columns = self.shapefile.columns
        for col in columns:
            print(self.shapefile[col].head())

    def showAllValuesInColumn(self,index):
        column = self.shapefile.columns[index]
        columns = self.shapefile.columns
        for col in range(0,len(columns)):
            print(col, columns[col])

        for colu in self.shapefile[column].unique():
            print(colu)


    def geopandastocsv(self):
        self.shapefile.copy().drop('geometry',axis=1).to_csv(r'plswork_pr.csv')
    def showWholeMap(self):

        self.shapefile.plot(cmap='jet', edgecolor='black')
        plt.show()



if __name__ =="__main__":
    explorer = ShapeFileExp()
    # toolkit.showAllCities()
    # explorer.showAllValuesInColumn(10)
    explorer.geopandastocsv()
else:
    print("test wrong")