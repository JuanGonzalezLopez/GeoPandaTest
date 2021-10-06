import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygeos
from shapely.geometry import Polygon, MultiLineString, MultiPolygon
from scipy.spatial import Delaunay
from shapely.ops import polygonize, cascaded_union
import h3pandas


class PuertoRicoGISCode():
    def __init__(self, puertorico: object, roads: object, column: str = 'ADM1_ES') -> object:
        '''
            This is the first step to building your Grid zones
            There are a couple of methods here to produce different types of zone divisions
            The simplest one is a square grid zone division
            The complex version is a hexagonal grid zone

            Pros and cons:
                Square Grid system
                    (Pros):
                        * simple and faster
                        * resizing is much more flexible
                    (Cons):
                        * simpler means it loses information when it comes to the Machine Learning portion
                        * Bigger square grid sizes suffer more from this problem
                Hexagon Grid zonal system
                    (Pros):
                        * Much more structured
                        * More information is retained due to it's geometry
                        * Big Tech companies like Uber use this type of zonal system

                    (Cons):
                        * Resizing is much more strict, it may be too small or too big for some zonal systems. (I think it has an exponential integer scaling)
                        * This would result in having hexagonal sizes that will cover too much, and other systems that would be too small.
                        * A bit less efficient
                        * Code comes from the H3pandas library, which is very limiting and lacking flexibility.


            This code will have lots of methods/functions that will help examine certain aspects of the shapefile data

            This code has been structured to work for Puerto Rico as a base, to expand on any place that isn't Puerto Rico would require
            new shapefile data from the target location.

            This code will have as inputs two separate shapefiles: The Cities shapefile and the roads shapefile.
            The cities will contain all 78 cities from Puerto Rico, while the roads will include every single roadway in Puerto Rico.
            The latter can help a future algorithm to divide zones much more effectively.

            Service areas wouldn't usually cover a whole city, in the case that a shapefile (or related file) isn't fed into the code, it will automatically take all the ride data's coordinates and convert them to points.
            (TODO program a function to recieve a service area shapefile.)
            Those points will be used to form a concave/convex hull that will approximate the service area without any other user input.


            To the code:

                The constructor will receive the two inputs as mentioned above: Cities shapefile | Roads Shapefile
                In this specific shapefile we need to identify the 'column' that has the name of the city for the respective geometry.



                :param puertorico: The shapefile (from the internet) that has all the cities of Puerto Rico
                :param roads: The shapefile (from the internet) that has all the roads of Puerto Rico
                :param column: Specifies the column of the PuertoRico shapefile that has the name of the cities

                :var self.cities: extracts the cities from said column inside the puertorico shapefile.

        '''

        # self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm0_2019.shp')
        self.puertorico = puertorico
        self.roads = roads
        self.cities_column = column
        self.cities = self.puertorico[self.cities_column]

    def showAllColumns(self):
        """
            Prints all the columns inside the PuertoRico shapefile
            Useful to quickly see all the columns inside the shapefile
        """
        columns = self.puertorico.columns
        for col in columns:
            print(self.puertorico[col].head())

    def showCities(self):
        """
            Prints a sample of the cities inside the PuertoRico shapefile
            Prints the amount of cities that the shapefile contains.
        """

        print(self.cities)
        print("There are " + str(len(self.cities)) + " cities.")

    def showAllCities(self):
        """
            Will print ALL the cities inside the PuertoRico shapefile instead of a sample
        """

        for index, row in self.puertorico.iterrows():
            print(index, row[self.cities_column])
        print("There are " + str(len(self.cities)) + " cities.")

    def showWholeMap(self):
        """
            Plots a map of the shapefile geometry.
            In this case it will plot Puerto Rico and it's cities

        """

        self.puertorico.plot(cmap='jet', edgecolor='black', column=self.cities_column)
        plt.show()

    def showSimpleCity(self, city: str = '', index: int = -1) -> object:
        """
            Will Plot the city that is specified in the inputs.
            Two ways of specifying a city:

        :param city: String of the name of the city. Must be written in the same way it is in the cities' column
        :param index: Integer of the index of the city in the cities' column
        :rtype: geopandas of the specified city

            if index is specified, it will override any argument in the city parameter

            HINT: Use the showAllCities if you don't know any cities nor their index in the column. It will print out the name with the index next to it.
        """
        self.city = city
        if (0 <= index <= len(
                self.cities)):  # Check if the index is between 0 or the amount of cities that the shapefile has, otherwise it will use the city's string argument to search the city's name
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(
            drop=True)  # Finds the specified city's geometry inside the shapefile
        # print(self.df_city)
        for col in self.df_city.columns:
            print(col, " - ", self.df_city[col])

        self.df_city.plot(color='red', edgecolor='black')  # plots the city's geometry

        plt.show()  # shows it
        return self.df_city

    def showSpecificCity(self, city: str = '', index: int = -1) -> object:

        """
            Will Plot the city WITH ROADS that is specified in the inputs.
            Two ways of specifying a city:

        :param city: String of the name of the city. Must be written in the same way it is in the cities' column
        :param index: Integer of the index of the city in the cities' column
        :returns: geopandas of the specified city

            if index is specified, it will override any argument in the city parameter

            HINT: Use the showAllCities if you don't know any cities nor their index in the column. It will print out the name with the index next to it.
        """
        self.city = city
        if (0 <= index <= len(
                self.cities)):  # Check if the index is between 0 or the amount of cities that the shapefile has, otherwise it will use the city's string argument to search the city's name
            self.city = self.cities[index]

        self.df_city = self.showSimpleCity(self.city)

        self.df_city_roads = gpd.clip(self.roads, self.df_city, keep_geom_type=True)
        # self.df_city_roads = gpd.join(gpd.clip(self.roads,self.df_city,keep_geom_type=True),self.df_city) # prototype - untested. may combine both clipped roads and the city's outline

        fig, ax = plt.subplots(figsize=(12, 8))

        self.df_city_roads.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')
        # self.df_city.plot(color='red', edgecolor='black')

        plt.show()

    def points_from_polygons(self, polygons: object) -> object:
        """
            This will extract all points from any polygon input
            :param polygons: geometry/polygon
            :return: Points from the geometry/polygon
        """
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

    def showGridCity(self, city: str = '', index: int = -1, clip: bool = True, cuadritos: int = 50) -> object:
        """

        :param city: String of the name of the city. Must be written in the same way it is in the cities' column
        :param index: Integer of the index of the city in the cities' column
        :param clip: Identify if you want to clip, or join. By default it will clip
        :param cuadritos: Identify the size, the higher the number the SMALLER the squares/grid
        :return: the square grid of city.
        """
        self.city = city
        if (0 <= index <= len(
                self.cities)):  # Check if the index is between 0 or the amount of cities that the shapefile has, otherwise it will use the city's string argument to search the city's name
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(
            drop=True)  # Finds the specified city's geometry inside the shapefile

        """
            Will create a grid of squares from the Xmin to the Xmax, Ymin to the Ymax
            These min and max will be found in the total_bounds of the city
        """
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

        self.grid = gpd.GeoDataFrame(
            {self.cities_column: self.city, 'geometry': polygons})  # Creates a Geopandas of the Grid squares
        """
            Will take the geopandas of the grid squares, clip the the grid using the boundaries of the city.
        """
        if clip:
            self.joined = gpd.clip(self.grid, self.df_city)
        else:
            self.joined = gpd.sjoin(self.grid, self.df_city)

        # self.joined = gpd.clip(self.df_city, self.joined)

        """
            Plots the city with the grid system on top
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        self.joined.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')

        plt.savefig('./Images_plots/GridCity.png', format='png', dpi=1200)
        plt.show()
        return self.joined

    # def hexcity(self, city: str = '', index: int = -1, clip: bool = False, cuadritos: int = 250) -> object:
    #     """
    #
    #     :param city: String of the name of the city. Must be written in the same way it is in the cities' column
    #     :param index: Integer of the index of the city in the cities' column
    #     :param clip: Identify if you want to clip, or join. By default it will clip
    #     :param cuadritos: Please use a high amount, this will depend on how many squares will be registered by the h3pandas methods. if there is a low count of points, there will be gaps of hexagons.
    #     :return: the square grid of city.
    #     """
    #     self.city = city
    #     if (0 <= index <= len(self.cities)):
    #         self.city = self.cities[index]
    #
    #     print("City: ", self.city)
    #
    #     self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)
    #
    #     xmin, ymin, xmax, ymax = self.df_city.total_bounds
    #     length = (xmax - xmin) / cuadritos
    #     wide = (ymax - ymin) / cuadritos
    #     # print((xmax-xmin),(ymax-ymin))
    #     cols = list(np.arange(xmin, xmax + wide, wide))
    #     rows = list(np.arange(ymin, ymax + length, length))
    #
    #     polygons = []
    #     for x in cols[:-1]:
    #         for y in rows[:-1]:
    #             polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))
    #
    #     self.grid = gpd.GeoDataFrame({self.cities_column: self.city, 'geometry': polygons})
    #
    #
    #
    #     if clip:
    #         self.joined = gpd.clip(self.grid, self.df_city)
    #     else:
    #         self.joined = gpd.sjoin(self.grid, self.df_city)
    #
    #
    #     points = self.points_from_polygons(self.joined.geometry)
    #     points = np.array(points)
    #     geopoints = {"lng": points[:, 0], "lat": points[:, 1]}
    #
    #     geopoints = pd.DataFrame(geopoints)
    #     reso = 9
    #     self.grid = geopoints.h3.geo_to_h3(reso)
    #     print(self.grid)
    #     self.grid = self.grid.drop(columns=['lng', 'lat']).groupby('h3_0' + str(reso)).sum()
    #     self.grid = self.grid.h3.h3_to_geo_boundary()
    #     print(self.grid)
    #     fig, ax = plt.subplots(figsize=(12, 8))
    #
    #     self.grid.plot(ax=ax)
    #     plt.show()
    #
    #     # self.joined = gpd.clip(self.df_city, self.joined)
    #     #
    #     # fig, ax = plt.subplots(figsize=(12, 8))
    #     #
    #     # self.joined.plot(ax=ax, color='red', edgecolor='black')
    #     # self.df_city.boundary.plot(ax=ax, color='black')
    #     #
    #     # plt.savefig('myimage.png', format='png', dpi=1200)
    #     # plt.show()
    #     # return self.joined
    def concave_hull(self, points_gdf, alpha=35):
        """
        Compute the concave hull (alpha shape) of a GeoDataFrame of points.
        Dude trust me.

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

    def split_polygon(self, city: str = '', index: int = -1) -> object:

        """
            IGNORE!!!!!
                Used for the Mayaguez City, the shapefile had extra islands that didn't help in the analysis.
                This is a hard coded function and it was meant to get the polygon from the multipolygon geometry from the Mayaguez city
            :param city: String of the name of the city. Must be written in the same way it is in the cities' column
            :param index: Integer of the index of the city in the cities' column
            :return: the polygon inside the polygon
        """
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

    def createHullPoints(self, filename: str, target: str = "start",data=None) -> object:
        """
        Will extract the coordinate floats from the columns inside the ride data and convert them to points.
            :param filename: the name of the data excel file
            :param target: specify if you want the starting coordinates or the ending coordinates
            :return: Geopandas geodataframe of points extracted from the coordinates
        """
        if(data!=None):
            df = data
        else:
            df = pd.read_excel(filename)

        lat = "new_" + target + "_lat"
        long = "new_" + target + "_long"
        points = df[[lat, long]]
        points = points[points[lat] >= 17].reset_index(drop=True)
        points = points.rename(columns={lat: "Latitude", long: "Longitude"})
        points.to_csv("./ride_data/Hull_" + target + ".csv", index=False)
        points = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points.Longitude, points.Latitude))
        return points

    def createPointsInGridData(self, show: bool = False,
                               filename: str = './Data/processed_ride_data_dic_24.xlsx',data=None) -> object:
        """

        :param show: Specify if you want to plot (saves time when False)
        :param filename: filename of the Ride Data
        :return:

        """
        # extract points from the coordinates columns
        points = self.createHullPoints(filename=filename,data=data)
        hull = self.concave_hull(points, alpha=250)
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
        return grid_shp, points_shp

    def createCountPerZone(self):
        Grids, Zone_Points = self.createPointsInGridData()
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

    def showGridCityRoads(self, city='', index=-1, clip=False):
        self.city = city
        if (0 <= index <= len(self.cities)):
            self.city = self.cities[index]

        print("City: ", self.city)

        self.df_city = self.puertorico.loc[self.puertorico[self.cities_column] == self.city].reset_index(drop=True)

        xmin, ymin, xmax, ymax = self.df_city.total_bounds
        cuadritos = 250
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
        self.df_city_roads = gpd.clip(self.roads, self.df_city, keep_geom_type=True)

        if clip:
            self.joined = gpd.clip(self.grid, self.df_city_roads)
        else:
            self.joined = gpd.sjoin(self.grid, self.df_city_roads)

        # self.joined = gpd.clip(self.df_city, self.joined)

        fig, ax = plt.subplots(figsize=(12, 8))

        self.joined.plot(ax=ax, color='red', edgecolor='black')
        self.df_city.boundary.plot(ax=ax, color='black')

        plt.savefig('myimage.png', format='png', dpi=1200)
        plt.show()
        # grid.to_file("GridCities/"+str(self.city)+ ".shp")

    def honeycomb(self, reso=10, show=True, filename='./Data/processed_ride_data_dic_24.xlsx',data=None):
        if (0 <= reso < 10):
            resostring = "h3_0" + str(reso)
        else:
            resostring = "h3_" + str(reso)



        pointsrides = self.createHullPoints(filename)
        hull = self.concave_hull(pointsrides, alpha=250)

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
        self.maya_hex_city = maya_grid_buffer
        self.points = pointsrides
        self.buffer = buffer
        if (show):
            fig, ax = plt.subplots(figsize=(12, 8))

            self.grid.plot(ax=ax, color='yellow', edgecolor='black')

            self.buffer.boundary.plot(ax=ax, edgecolor='black')

            pointsrides.plot(ax=ax, color='red', edgecolor='black')

            plt.savefig('honeycomb.png', format='png', dpi=1200)
            plt.show()

    def createPointsInHexData(self, reso=10, show=False, filename='./Data/processed_ride_data_dic_24.xlsx',data=None):
        self.honeycomb(reso=reso, show=show, filename=filename,data=data)

        temp_maya = self.grid.reset_index()
        print(temp_maya)
        mayageo = self.maya_hex_city['geometry']
        # temp_maya = temp_maya.drop(['index_right'], axis='columns')
        grid_shp = {}
        grid_id = []
        grid_geo = []
        points_shp = {}
        grid_id_points = []
        points_geo = []

        for i in range(0, mayageo.size):

            invd_grid_square = temp_maya.iloc[[i]]
            # print(self.points)
            # print(invd_grid_square)
            points_in_square = gpd.sjoin(self.points, invd_grid_square, op='within')
            print(points_in_square)

            fig, ax = plt.subplots(figsize=(12, 8))
            invd_grid_square.plot(ax=ax, color='yellow', edgecolor='black')
            points_in_square.plot(ax=ax, color='red', edgecolor='black')
            plt.show()

            grid_string = "hexa_" + str(i)
            grid_id.append(grid_string)
            grid_geo.append(invd_grid_square.reset_index(drop=True)['geometry'][0])

            if not (points_in_square.empty):
                try:
                    for geo in points_in_square['geometry']:
                        grid_id_points.append(grid_string)
                        points_geo.append(geo)
                except:
                    pass

        if (show):
            fig, ax = plt.subplots(figsize=(12, 8))

            self.grid.plot(ax=ax, color='yellow', edgecolor='black')

            self.buffer.boundary.plot(ax=ax, edgecolor='black')

            self.points.plot(ax=ax, color='red', edgecolor='black')

            plt.savefig('honeycomb.png', format='png', dpi=1200)
            plt.show()

        grid_shp['Hex_ID'] = grid_id
        grid_shp['geometry'] = grid_geo
        points_shp['Hex_ID'] = grid_id_points
        points_shp['geometry'] = points_geo

        grid_shp = pd.DataFrame(grid_shp)
        points_shp = pd.DataFrame(points_shp)

        grid_shp = gpd.GeoDataFrame(grid_shp)
        points_shp = gpd.GeoDataFrame(points_shp)

        grid_shp.to_file('Grid_Points/Hex_with_IDs.shp')
        points_shp.to_file('Grid_Points/Points_with_HexIDs.shp')
        print(points_shp)
        return grid_shp, points_shp

    def ZoneIndicator(self, reso=10, show=False, filename='./Data/processed_ride_data_dic_24.xlsx',
                      output="ride_hex_data.csv"):
        self.honeycomb(reso=reso, show=show, filename=filename)

        temp_maya = self.grid.reset_index()
        print(temp_maya)
        mayageo = self.maya_hex_city['geometry']
        # temp_maya = temp_maya.drop(['index_right'], axis='columns')
        # grid_df = {}
        # grid_id = []
        # grid_geo = []
        points_df = {}
        grid_id_points = []
        ride_id = []
        target = []
        points_geo = []
        for i in range(0, self.size):

            invd_grid_square = temp_maya.iloc[[i]]
            # print(self.points)
            # print(invd_grid_square)
            points_in_square = gpd.sjoin(self.points, invd_grid_square, op='within')
            # if(show):
            #     fig, ax = plt.subplots(figsize=(12, 8))
            #     invd_grid_square.plot(ax=ax, color='yellow', edgecolor='black')
            #     points_in_square.plot(ax=ax, color='red', edgecolor='black')
            #     plt.show()

            grid_string = "hexa_" + str(i)
            # grid_id.append(grid_string)
            # grid_geo.append(invd_grid_square.reset_index(drop=True)['geometry'][0])

            if not (points_in_square.empty):
                try:
                    for index, row in points_in_square.iterrows():
                        grid_id_points.append(grid_string)
                        points_geo.append(row['geometry'])
                        ride_id.append(row['ride_id'])
                        target.append(row['target'])
                except:
                    pass

        print(grid_id_points)
        points_df['Hex_ID'] = grid_id_points
        points_df['ride_id'] = ride_id
        points_df['target'] = target
        points_df['geometry'] = points_geo

        points_df = pd.DataFrame(points_df)
        print(points_df)
        points_df.to_csv(output, index=False)
        return points_df


if __name__ == "__main__":
    puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
    roads = gpd.read_file(r'PRRoads/hotosm_pri_roads_lines.shp')
    toolkit = PuertoRicoGISCode(puertorico, roads)
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
    # toolkit.honeycomb(reso=10)
    toolkit.createPointsInHexData(show=True)
    # Extras
    # toolkit.showAllColumns()
    # toolkit.split_polygon(index=49)
else:
    print("test wrong")