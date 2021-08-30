from shapely.geometry import Point, LineString, Polygon
import numpy as np
from numpy import ndarray
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt

import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/gustavocalderon/PycharmProjects/GeoPandaTest/ride_data/HullEx.csv')

rng = np.random.default_rng()
points = rng.random((30, 2))   # 30 random points in 2-D
# points = df.to_numpy()
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
gdf.convex_hull
gdf.plot()
plt.show()
# df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
# df['Coordinates'] = df['Coordinates'].apply(Point)
# hull = ConvexHull(points)
# df = df.fillna(0)
#
# plt.plot(points[:,0], points[:,1], 'o')
# for simplex in hull.simplices:
#     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
# plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
# plt.show()
# print(points)
# geopandas.GeoSeries.buffer(points)

# s = geopandas.GeoSeries(
#      [
#      Point(0, 0),
#         LineString([(1, -1), (1, 0), (2, 0), (2, 1)]),
#         Polygon([(3, -1), (4, 0), (3, 1)]),
#     ] )
# fix, axs = plt.subplots(
#     3, 2, figsize=(12, 12), sharex=True, sharey=True
# )
# for ax in axs.flatten():
#     s.plot(ax=ax)
#     ax.set(xticks=[], yticks=[])
# s.buffer(0.8)
# s.plot()
# plt.show()