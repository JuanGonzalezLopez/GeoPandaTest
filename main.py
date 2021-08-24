import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Polygon

class PuertoRicoGISCode():
    def __init__(self):
        # self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm0_2019.shp')
        self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
        self.roads = gpd.read_file(r'PRRoads/hotosm_pri_roads_lines.shp')
        self.cities_column = 'ADM1_ES'
        self.cities = self.puertorico[self.cities_column]
        print(self.cities)
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
        print(self.df_city)
        for col in self.df_city.columns:
            print(col," - ", self.df_city[col])

        self.df_city_roads = gpd.clip(self.roads,self.df_city,keep_geom_type=True)
        fig, ax = plt.subplots(figsize=(12, 8))


        self.df_city_roads.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')
        # self.df_city.plot(color='red', edgecolor='black')

        plt.show()

    def split_polygon(self,city='',index=-1):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        polygons = list(self.df_city['geometry'][0])


        '''
            0. Isla de Desecheo Marine Reserve
            1. Mayaguez
            2. Isla Monito
            4. Mona
        '''


        self.puertorico['geometry'].iloc[index] = polygons[1]
        self.puertorico.to_file('Shapefiles/pri_admbnda_adm1_2019.shp')
        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)
        self.df_city.plot(color='red', edgecolor='black')
        plt.show()

    def showSpecificCity(self,city='',index=-1):
        self.city = city
        if(0<=index<=len(self.cities)):
            self.city=self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column]==self.city].reset_index(drop=True)
        print(self.df_city)
        for col in self.df_city.columns:
            print(col," - ", self.df_city[col])

        self.df_city_roads = gpd.clip(self.roads,self.df_city,keep_geom_type=True)
        fig, ax = plt.subplots(figsize=(12, 8))


        self.df_city_roads.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')
        # self.df_city.plot(color='red', edgecolor='black')

        plt.show()
    def showGridCityRoads(self,city='',index=-1,clip=False):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        xmin, ymin, xmax, ymax =self.df_city.total_bounds
        length = (xmax-xmin)/250
        wide = (ymax-ymin)/250
        # print((xmax-xmin),(ymax-ymin))
        cols = list(np.arange(xmin, xmax + wide, wide))
        rows = list(np.arange(ymin, ymax + length, length))

        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))



        self.grid = gpd.GeoDataFrame({self.cities_column: self.city,'geometry': polygons})
        self.df_city_roads = gpd.clip(self.roads, self.df_city, keep_geom_type=True)

        if clip:
            self.joined = gpd.clip(self.grid,self.df_city_roads)
        else:
            self.joined = gpd.sjoin(self.grid,self.df_city_roads)

        # self.joined = gpd.clip(self.df_city, self.joined)

        fig, ax = plt.subplots(figsize=(12, 8))

        self.joined.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')


        plt.savefig('myimage.png', format='png', dpi=1200)
        plt.show()
        # grid.to_file("GridCities/"+str(self.city)+ ".shp")

if __name__ =="__main__":
    toolkit = PuertoRicoGISCode()
    # toolkit.showAllCities()
    toolkit.showGridCityRoads(index=49)
    # toolkit.showAllCities()
else:
    print("test wrong")