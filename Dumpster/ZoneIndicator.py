import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygeos
from shapely.geometry import Polygon,MultiLineString,MultiPolygon
from scipy.spatial import Delaunay
from shapely.ops import polygonize, cascaded_union
import h3pandas




class testingZones():
    def __init__(self):
        # self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm0_2019.shp')
        self.puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')
        self.roads = gpd.read_file(r'PRRoads/hotosm_pri_roads_lines.shp')
        self.cities_column = 'ADM1_ES'
        self.cities = self.puertorico[self.cities_column]
        print(self.cities)

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
    def hexcity(self,points,reso=10, show=True,filename='./ride_data/processed_ride_data_dic_24.xlsx'):
        if (0<=reso<10):
            resostring="h3_0"+str(reso)
        else:
            resostring="h3_"+str(reso)

        hull = self.concave_hull(points,alpha=250)


        mayaguez_grid = self.showGridCity(index=49, cuadritos=250)

        buffer = hull.buffer(.0005)

        bufferdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(buffer))
        maya_grid_buffer = gpd.sjoin(mayaguez_grid, bufferdf)

        points = self.points_from_polygons(maya_grid_buffer.geometry)
        points = np.array(points)
        geopoints = {"lng": points[:, 0], "lat": points[:, 1]}

        geopoints = pd.DataFrame(geopoints)
        self.hex = geopoints.h3.geo_to_h3(reso)
        print(self.hex)
        self.hex = self.hex.drop(columns=['lng', 'lat']).groupby(resostring).sum()
        self.hex = self.hex.h3.h3_to_geo_boundary()
        self.maya_hex_city = maya_grid_buffer
        # self.points = pointsrides
        self.buffer = buffer


        if (show):
            fig, ax = plt.subplots(figsize=(12, 8))

            self.hex.plot(ax=ax, color='yellow', edgecolor='black')

            self.buffer.boundary.plot(ax=ax, edgecolor='black')

            # pointsrides.plot(ax=ax, color='red', edgecolor='black')

            plt.savefig('honeycomb.png', format='png', dpi=1200)
            plt.show()
        return self.hex


    def createHullPoints(self,filename,target="start"):
        lat = "new_"+target+"_lat"
        long = "new_"+target+"_long"

        df = pd.read_excel(filename)
        df['target'] = target

        points = df[['ride_id','target',lat,long]]

        points = points.rename(columns={lat: "Latitude", long: "Longitude"})



        return points

    def createHullGeo(self,points,target="start"):
        points = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points.Longitude, points.Latitude))
        return points

    def StartEndConcat(self,filename='./ride_data/processed_ride_data_dic_24.xlsx'):
        pointsridesStart = self.createHullPoints(filename,target='start')
        pointsridesEnd = self.createHullPoints(filename,target='end')
        allpoints = pd.concat([pointsridesStart,pointsridesEnd]).reset_index(drop=True)
        allpoints= self.createHullGeo(allpoints)
        print(allpoints)


        allpoints = allpoints[(allpoints["Latitude"] >= 17) & (allpoints["Longitude"] <= -65)].reset_index(drop=True)
        allpoints.to_csv("./ExtraCSVs/allpoints.csv",index=False)

        print(allpoints)

        allpoints.plot()
        plt.show()

        return allpoints

    def honeycomb(self,reso=10, show=True,filename='./ride_data/processed_ride_data_dic_24.xlsx'):
        if (0<=reso<10):
            resostring="h3_0"+str(reso)
        else:
            resostring="h3_"+str(reso)

        pointsrides = self.StartEndConcat(filename)
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
        temp = self.grid.copy()
        self.size= len(temp.geometry.values)
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




    def ZoneIndicator(self,reso=10,show=False,filename='./ride_data/processed_ride_data_dic_24.xlsx'):
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
                    for index,row in points_in_square.iterrows():
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
        points_df.to_csv("ride_hex_data.csv",index=False)
        return points_df









if __name__=="__main__":
    tool = testingZones()
    tool.ZoneIndicator()

















