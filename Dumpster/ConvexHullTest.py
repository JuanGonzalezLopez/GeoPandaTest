from shapely.geometry import Point, LineString, Polygon
import numpy as np
from numpy import ndarray
from scipy.spatial import ConvexHull, convex_hull_plot_2d,Delaunay
import matplotlib.pyplot as plt
from shapely.ops import polygonize, cascaded_union

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,MultiLineString
import matplotlib.pyplot as plt
import pygeos


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
df = pd.read_csv('../ride_data/HullEx.csv')
print(df)
df = df[df['Latitude'] >= 17].reset_index(drop=True)
print(df[df['Latitude'] >= 17])
#
# rng = np.random.default_rng()
# points = rng.random((30, 2))   # 30 random points in 2-D
# points = df.to_numpy()

#
points = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
#
# points = df.values
print(points)

hull = concave_hull(points,alpha=350)

fig, ax = plt.subplots(figsize=(12, 8))


hull.buffer(.0005).plot(ax=ax, edgecolor='red')
hull.plot(ax=ax, edgecolor='black')

points.plot(ax=ax, color='red', edgecolor='black')

# plt.savefig('myimage.png', format='png', dpi=1200)
plt.show()

# hull = ConvexHull(points,incremental=True)
# print(hull.simplices)
# plt.plot(points[:,0], points[:,1], 'o')
#
# for simplex in hull.simplices:
#     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
#     print(simplex)
# plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')

# plt.show()
# df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
# df['Coordinates'] = df['Coordinates'].apply(Point)