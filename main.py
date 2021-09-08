import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygeos
from shapely.geometry import Polygon,MultiLineString,MultiPolygon
from scipy.spatial import Delaunay
from shapely.ops import polygonize, cascaded_union
import h3pandas
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
    def showSimpleCity(self,city='',index=-1):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)
        print(self.df_city)
        for col in self.df_city.columns:
            print(col, " - ", self.df_city[col])

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
    def points_from_polygons(self, polygons):
        points = []
        for mpoly in polygons:
            if isinstance(mpoly, MultiPolygon):
                polys = list(mpoly)
            else:
                polys = [mpoly]
            for polygon in polys:
                for point in polygon.exterior.coords:
                    points.append(list(point))
                for interior in polygon.interiors:
                    for point in interior.coords:
                        points.append(list(point))
        return points

    def showGridCity(self,city='',index=-1,clip=True, cuadritos=50):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        xmin, ymin, xmax, ymax = self.df_city.total_bounds
        length = (xmax - xmin) / cuadritos
        wide = (ymax - ymin) / cuadritos
        # print((xmax-xmin),(ymax-ymin))
        cols = list(np.arange(xmin, xmax + wide, wide))
        rows = list(np.arange(ymin, ymax + length, length))

        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))

        self.grid = gpd.GeoDataFrame({self.cities_column: self.city, 'geometry': polygons})

        if clip:
            self.joined = gpd.clip(self.grid, self.df_city)
        else:
            self.joined = gpd.sjoin(self.grid, self.df_city)

        # self.joined = gpd.clip(self.df_city, self.joined)

        fig, ax = plt.subplots(figsize=(12, 8))

        self.joined.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')

        plt.savefig('myimage.png', format='png', dpi=1200)
        plt.show()
        return self.joined



    def hexcity(self,city='',index=-1,clip=False, cuadritos=50):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        xmin, ymin, xmax, ymax = self.df_city.total_bounds
        length = (xmax - xmin) / cuadritos
        wide = (ymax - ymin) / cuadritos
        # print((xmax-xmin),(ymax-ymin))
        cols = list(np.arange(xmin, xmax + wide, wide))
        rows = list(np.arange(ymin, ymax + length, length))

        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))

        self.grid = gpd.GeoDataFrame({self.cities_column: self.city, 'geometry': polygons})



        if clip:
            self.joined = gpd.clip(self.grid, self.df_city)
        else:
            self.joined = gpd.sjoin(self.grid, self.df_city)


        points = self.points_from_polygons(self.joined.geometry)
        points = np.array(points)
        geopoints = {"lng": points[:, 0], "lat": points[:, 1]}

        geopoints = pd.DataFrame(geopoints)
        reso = 9
        self.grid = geopoints.h3.geo_to_h3(reso)
        print(self.grid)
        self.grid = self.grid.drop(columns=['lng', 'lat']).groupby('h3_0' + str(reso)).sum()
        self.grid = self.grid.h3.h3_to_geo_boundary()
        print(self.grid)
        fig, ax = plt.subplots(figsize=(12, 8))

        self.grid.plot(ax=ax)
        plt.show()

        # self.joined = gpd.clip(self.df_city, self.joined)
        #
        # fig, ax = plt.subplots(figsize=(12, 8))
        #
        # self.joined.plot(ax=ax, color='red', edgecolor='black')
        # self.df_city.boundary.plot(ax=ax, color='black')
        #
        # plt.savefig('myimage.png', format='png', dpi=1200)
        # plt.show()
        # return self.joined
    def concave_hull(self, points_gdf, alpha=35):
        """
        Compute the concave hull (alpha shape) of a GeoDataFrame of points.


        Parameters
        ==========
        points_gdf : gpd.GeoDataFrame
          GeoDataFrame of points.

        alpha: int

          alpha value to influence the gooeyness of the border. Smaller numbers
          don't fall inward as much as larger numbers. Too large, and you lose everything!
        """
        if len(points_gdf) < 4:
            # When you have a triangle, there is no sense
            # in computing an alpha shape.
            return points_gdf.unary_union.convex_hull

        coords = pygeos.coordinates.get_coordinates(points_gdf.geometry.values.data)
        tri = Delaunay(coords)
        triangles = coords[tri.vertices]
        a = ((triangles[:, 0, 0] - triangles[:, 1, 0]) ** 2 + (triangles[:, 0, 1] - triangles[:, 1, 1]) ** 2) ** 0.5
        b = ((triangles[:, 1, 0] - triangles[:, 2, 0]) ** 2 + (triangles[:, 1, 1] - triangles[:, 2, 1]) ** 2) ** 0.5
        c = ((triangles[:, 2, 0] - triangles[:, 0, 0]) ** 2 + (triangles[:, 2, 1] - triangles[:, 0, 1]) ** 2) ** 0.5
        s = (a + b + c) / 2.0
        areas = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        circums = a * b * c / (4.0 * areas)
        filtered = triangles[circums < (1.0 / alpha)]
        edge1 = filtered[:, (0, 1)]
        edge2 = filtered[:, (1, 2)]
        edge3 = filtered[:, (2, 0)]
        edge_points = np.unique(np.concatenate((edge1, edge2, edge3)), axis=0).tolist()
        m = MultiLineString(edge_points)
        triangles = list(polygonize(m))
        return gpd.GeoDataFrame({"geometry": [cascaded_union(triangles)]}, index=[0], crs=points_gdf.crs)
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
            3. Mona
        '''


        self.puertorico['geometry'].iloc[index] = polygons[1]
        self.puertorico.to_file('Shapefiles/pri_admbnda_adm1_2019.shp')
        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)
        self.df_city.plot(color='red', edgecolor='black')
        plt.show()

    def createHullPoints(self,filename):
        df = pd.read_excel(filename)
        points = df[['new_start_lat', 'new_start_long']]
        points = points[points['new_start_lat'] >= 17].reset_index(drop=True)
        points = points.rename(columns={"new_start_lat": "Latitude", "new_start_long": "Longitude"})
        points.to_csv("./ride_data/Hull.csv",index=False)
        points = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points.Longitude, points.Latitude))
        return points

    def createPointsInGridData(self,show=False):
        points = self.createHullPoints('./ride_data/processed_ride_data_dic_24.xlsx')
        hull = self.concave_hull(points,alpha=250)
        mayaguez_grid = self.showGridCity(index=49, cuadritos=225)
        buffer = hull.buffer(.0005)

        bufferdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(buffer))
        maya_grid_buffer = gpd.sjoin(mayaguez_grid, bufferdf)

        temp_maya = maya_grid_buffer.reset_index(drop=True)
        mayageo = maya_grid_buffer['geometry']
        temp_maya = temp_maya.drop(['index_right'], axis='columns')
        grid_shp = {}
        grid_id = []
        grid_geo = []
        points_shp = {}
        grid_id_points = []
        points_geo = []
        for i in range(0, mayageo.size):

            invd_grid_square = temp_maya.iloc[[i]]

            # print(invd_grid_square)
            # invd_grid_square.plot()
            # plt.show()
            points_in_square = gpd.sjoin(points, invd_grid_square, op='within')
            grid_string = "grid_" + str(i)
            grid_id.append(grid_string)
            grid_geo.append(invd_grid_square.reset_index(drop=True)['geometry'][0])

            if not (points_in_square.empty):
                try:
                    for geo in points_in_square['geometry']:
                        grid_id_points.append(grid_string)
                        points_geo.append(geo)
                except:
                    pass
        grid_shp['Grid_ID'] = grid_id
        grid_shp['geometry'] = grid_geo
        points_shp['Grid_ID'] = grid_id_points
        points_shp['geometry'] = points_geo

        grid_shp = pd.DataFrame(grid_shp)
        points_shp = pd.DataFrame(points_shp)


        grid_shp = gpd.GeoDataFrame(grid_shp)
        points_shp = gpd.GeoDataFrame(points_shp)

        if (show):
            fig, ax = plt.subplots(figsize=(12, 8))

            maya_grid_buffer.plot(ax=ax, color='yellow', edgecolor='black')

            buffer.boundary.plot(ax=ax, edgecolor='black')

            points.plot(ax=ax, color='red', edgecolor='black')

            # plt.savefig('myimage.png', format='png', dpi=1200)
            plt.show()
        grid_shp.to_file('Grid_Points/Grid_with_IDs.shp')
        points_shp.to_file('Grid_Points/Points_with_GridIDs.shp')
        print(points_shp)
        return grid_shp,points_shp

    def createCountPerZone(self):
        Grids,Zone_Points = self.createPointsInGridData()
        print(Grids)
        print(Zone_Points)
        zones = []
        counter = []

        for zone in Grids['Grid_ID'].unique():
            count = Zone_Points.loc[Zone_Points['Grid_ID'] == zone].size

            zones.append(zone)
            counter.append(count)

        temp_dict = {}
        temp_dict['Grid_ID'] = zones
        temp_dict['ride_counter'] = counter

        ride_per_zone = pd.DataFrame(temp_dict)
        ride_per_zone.to_csv("./ride_data/ride_per_zone.csv", index=False)
        return ride_per_zone



    def showGridCityRoads(self,city='',index=-1,clip=False):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        xmin, ymin, xmax, ymax =self.df_city.total_bounds
        cuadritos = 250
        length = (xmax-xmin)/cuadritos
        wide = (ymax-ymin)/cuadritos
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
    def honeycomb(self,reso=10, show=True):
        if (0<=reso<10):
            resostring="h3_0"+str(reso)
        else:
            resostring="h3_"+str(reso)

        pointsrides = self.createHullPoints('./ride_data/processed_ride_data_dic_24.xlsx')
        hull = self.concave_hull(pointsrides,alpha=250)


        mayaguez_grid = self.showGridCity(index=49, cuadritos=250)




        buffer = hull.buffer(.0005)

        bufferdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(buffer))
        maya_grid_buffer = gpd.sjoin(mayaguez_grid, bufferdf)

        points = self.points_from_polygons(maya_grid_buffer.geometry)
        points = np.array(points)
        geopoints = {"lng": points[:, 0], "lat": points[:, 1]}

        geopoints = pd.DataFrame(geopoints)
        self.grid = geopoints.h3.geo_to_h3(reso)
        print(self.grid)
        self.grid = self.grid.drop(columns=['lng', 'lat']).groupby(resostring).sum()
        self.grid = self.grid.h3.h3_to_geo_boundary()


        if (show):
            fig, ax = plt.subplots(figsize=(12, 8))

            self.grid.plot(ax=ax, color='yellow', edgecolor='black')

            buffer.boundary.plot(ax=ax, edgecolor='black')

            pointsrides.plot(ax=ax, color='red', edgecolor='black')

            plt.savefig('honeycomb.png', format='png', dpi=1200)
            plt.show()



if __name__ =="__main__":
    toolkit = PuertoRicoGISCode()
    # toolkit.showAllCities()
    #
    # # Step 2b. City
    # toolkit.showSimpleCity(index=49)
    # #
    # # # Step 3. Grids
    # toolkit.showGridCity(index=49,cuadritos=50)
    # #
    # # # Step 4. roads
    # toolkit.showSpecificCity(index=49)
    # #
    # # # Step 5. Roads with grids
    # toolkit.showGridCityRoads(index=49,cuadritos=250)
    #
    # Step 6. Create Zone Points data/shapefile
    toolkit.honeycomb(reso=10)

    # Extras
    # toolkit.showAllColumns()
    # toolkit.split_polygon(index=49)
else:
    print("test wrong")