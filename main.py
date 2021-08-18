import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Polygon


class PuertoRicoGISCode():

    def __init__(self):
        # self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm0_2019.shp')
        self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
        self.cities_column = 'ADM1_ES'
        self.cities = self.puertorico[self.cities_column]
    def showAllColumns(self):
        columns = self.puertorico.columns
        for col in columns:
            print(self.puertorico[col].head())

    def showCities(self):
        print(self.cities)
        print("There are " + str(len(self.cities))+" cities.")

    def showAllCities(self):
        for index,row in self.puertorico.iterrows():
            print(index, row[self.cities_column])
        print("There are " + str(len(self.cities))+" cities.")


    def showWholeMap(self):

        self.puertorico.plot(cmap='jet', edgecolor='black', column=self.cities_column)
        plt.show()

    def showSpecificCity(self,city='',index=-1):
        self.city = city
        if(0<=index<=len(self.cities)):
            self.city=self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column]==self.city].reset_index(drop=True)

        for col in self.df_city.columns:
            print(col," - ", self.df_city[col][0])

        self.df_city.plot(color='red', edgecolor='black')
        plt.show()


    def showGridCity(self,city='',index=-1,clip=True):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        xmin, ymin, xmax, ymax =self.df_city.total_bounds
        length = (xmax-xmin)/25
        wide = (ymax-ymin)/25
        # print((xmax-xmin),(ymax-ymin))
        cols = list(np.arange(xmin, xmax + wide, wide))
        rows = list(np.arange(ymin, ymax + length, length))

        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))

        self.grid = gpd.GeoDataFrame({self.cities_column: self.city,'geometry': polygons})

        if clip:
            self.joined = gpd.clip(self.grid,self.df_city)
        else:
            self.joined = gpd.sjoin(self.grid,self.df_city)

        self.joined.plot(color='red', edgecolor='black')
        plt.show()
        # grid.to_file("GridCities/"+str(self.city)+ ".shp")

if __name__ =="__main__":
    toolkit = PuertoRicoGISCode()
    # toolkit.showAllCities()
    toolkit.showGridCity(None,8)
else:
    print("test wrong")