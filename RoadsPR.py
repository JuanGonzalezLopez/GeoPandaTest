import geopandas as gpd
import matplotlib.pyplot as plt
# Importing an ESRIShapefile and plotting it using GeoPandas
districts = gpd.read_file(r'/Users/gustavocalderon/PycharmProjects/GeoPandaTest/PR/tl_2015_72_prisecroads.shp')
districts.plot(cmap = 'hsv', edgecolor = 'black')
plt.show()
#####################################


def showAllColumns(districts):
    columns = districts.columns
    for col in columns:
        print(districts[col].head())
print(showAllColumns(districts))

#########################################