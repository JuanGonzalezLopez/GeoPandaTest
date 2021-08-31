import geopandas as gpd
from geopandas.tools import sjoin
import pandas as pd
from scipy.spatial import ConvexHull, convex_hull_plot_2d,Delaunay
import matplotlib.pyplot as plt
from shapely.ops import polygonize, cascaded_union

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,MultiLineString
import matplotlib.pyplot as plt
import pygeos

from main import *
PuertoRico = PuertoRicoGISCode()
def concave_hull(points_gdf, alpha=35):
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


point = pd.read_csv('./ride_data/HullEx.csv')
print(point)
point = point[point['Latitude'] >= 17].reset_index(drop=True)
points= gpd.GeoDataFrame(
    point, geometry=gpd.points_from_xy(point.Longitude, point.Latitude))

mayaguez_grid = PuertoRico.showGridCity(index=49,cuadritos=225)
hull = concave_hull(points,alpha=325)
buffer = hull.buffer(.0005)

bufferdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(buffer))
print(bufferdf)
maya_grid_buffer = gpd.sjoin(mayaguez_grid, bufferdf)

print(maya_grid_buffer)
temp_maya =maya_grid_buffer.reset_index(drop=True)
mayageo = maya_grid_buffer['geometry']
print(mayageo.size)
temp_maya = temp_maya.drop(['index_right'],axis='columns')
print(temp_maya)
grid_shp = {}
grid_id = []
grid_geo=[]
points_shp = {}
grid_id_points = []
points_geo =[]
for i in range(0,mayageo.size):

    invd_grid_square = temp_maya.iloc[[i]]

    # print(invd_grid_square)
    # invd_grid_square.plot()
    # plt.show()
    points_in_square = gpd.sjoin(points,invd_grid_square,op='within' )
    grid_string = "grid_" + str(i)
    grid_id.append(grid_string)
    grid_geo.append(invd_grid_square.reset_index(drop=True)['geometry'][0])

    if not(points_in_square.empty):
        for geo in points_in_square['geometry']:
            grid_id_points.append(grid_string)
            points_geo.append(geo)


grid_shp['Grid_ID'] = grid_id
grid_shp['geometry'] = grid_geo
points_shp['Grid_ID'] = grid_id_points
points_shp['geometry'] = points_geo

grid_shp = pd.DataFrame(grid_shp)
points_shp = pd.DataFrame(points_shp)

print(grid_shp)
print(points_shp)
grid_shp = gpd.GeoDataFrame(grid_shp)
points_shp = gpd.GeoDataFrame(points_shp)
print(grid_shp)
grid_shp.to_file('Grid_Points/Grid_with_IDs.shp')
points_shp.to_file('Grid_Points/Points_with_GridIDs.shp')

# invd_grid_square = temp_maya.iloc[[394]]
# print(invd_grid_square)
# points_in_square = gpd.sjoin(invd_grid_square, points)
#
# points_in_square.plot(edgecolor='black')
plt.show()
fig, ax = plt.subplots(figsize=(12, 8))

maya_grid_buffer.plot(ax=ax,color='yellow', edgecolor='black')

buffer.boundary.plot(ax=ax, edgecolor='black')

points.plot(ax=ax, color='red', edgecolor='black')

# plt.savefig('myimage.png', format='png', dpi=1200)
plt.show()




# poly = gpd.GeoDataFrame.from_file('poly.shp')
# pointInPolys = sjoin(point, poly, how='left')
# pointSumByPoly = pointInPolys.groupby('PolyGroupByField')['fields', 'in', 'grouped', 'output'].agg(['sum'])