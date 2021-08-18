import geopandas as gpd
import matplotlib.pyplot as plt

# puertorico = gpd.read_file(r'Shapefiles/pri_admbndl_ALL_2019.shp')
puertorico = gpd.read_file(r'Shapefiles/pri_admbnda_adm1_2019.shp')

print(puertorico.head())

print(type(puertorico))
columns =puertorico.columns
for col in columns:
    print(puertorico[col].head())

puertorico.plot(cmap='jet', edgecolor='black', column = 'ADM1_ES')

plt.show()