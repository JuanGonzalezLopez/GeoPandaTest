import geopandas
from geopandas.tools import sjoin
point = geopandas.GeoDataFrame.from_file('point.shp') # or geojson etc
poly = geopandas.GeoDataFrame.from_file('poly.shp')
pointInPolys = sjoin(point, poly, how='left')
pointSumByPoly = pointInPolys.groupby('PolyGroupByField')['fields', 'in', 'grouped', 'output'].agg(['sum'])