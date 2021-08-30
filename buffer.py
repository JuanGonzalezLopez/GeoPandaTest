import geopandas
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt

s = geopandas.GeoSeries(
    [
        Point(0, 0),
        LineString([(1, -1), (1, 0), (2, 0), (2, 1)]),
        Polygon([(3, -1), (4, 0), (3, 1)]),
    ]
)
s

s.buffer(0.2)
s.plot()
plt.show()