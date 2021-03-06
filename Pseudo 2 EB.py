import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import csv


data = pd.read_csv('./Output/PrepoCluster.csv')

temp=data.groupby(['Hex_start','start_cluster']).size().reset_index(name='hex_cluster')

templog = temp.loc[temp['Hex_start'].isin(temp[temp.Hex_start.duplicated()]['Hex_start'])]

unique = templog['Hex_start'].drop_duplicates(keep='first').sort_values().reset_index(drop=True)


grouptemp = templog.groupby(['Hex_start'])


tempchange = grouptemp.apply(lambda grp: grp.loc[grp['hex_cluster'].idxmax()])[['Hex_start','start_cluster']].reset_index(drop=True)

nptempchange = tempchange['Hex_start'].to_numpy()
def clusterchange(row):
    if ( row['Hex_start'] in nptempchange):
        row['start_cluster'] = tempchange.loc[tempchange['Hex_start']==(row['Hex_start'])]['start_cluster'].to_numpy()[0]
    return row

data = data.apply(clusterchange,axis=1)

data.to_csv("./Output/Testtrimmingdata2.csv",index=False)

#
# # Create DataFrame
# df = pd.read_csv('./ride_data/HullEx.csv')
# # df = df.head(n=10)
# # print(df)
# df = df[df['Latitude'] >= 17].reset_index(drop=True)  # Remove invalid coordinates
# df.dropna(axis = 0, how = 'any', subset=['Latitude', 'Longitude'], inplace = True)
# X=df.loc[:,['Latitude','Longitude']]
# # X.head(10)
# print(X)
#
# # Elbow Curve: 12 Clusters
# # K_clusters = range(1,100)
# # kmeans = [KMeans(n_clusters=i) for i in K_clusters]
# # y_axis = df[['Latitude']]
# # x_axis = df[['Longitude']]
# # score = [kmeans[i].fit(y_axis).score(y_axis) for i in range(len(kmeans))]
# #
# # plt.plot(K_clusters, score)
# # plt.xlabel('Numero de Clusters')
# # plt.ylabel('Score')
# # plt.title('Elbow Curve')
# # plt.show()
#
#
# ###################################################
#
# kmeans = KMeans(n_clusters=12).fit(df)
# print(kmeans)
# centroids = kmeans.cluster_centers_
# print(centroids)
# plt.scatter(df['Longitude'], df['Latitude'], c = kmeans.labels_.astype(float),s=50, alpha=0.5)
# plt.scatter(centroids[:, 1], centroids[:, 0], c = 'red', s=50)
# print(len(kmeans.labels_.astype(float)))
# print(len(df["Longitude"]))
# df['Labels'] = kmeans.labels_.astype(float)
# print(df["Labels"])
# plt.show()
#
#
# ###############################################
#
# # Visualise
# # X.plot.scatter(x = 'Latitude', y = 'Longitude', c = labels, s=50, cmap = 'viridis')
# # plt.scatter(centers[:, 0], centers[:, 1], c = 'black', s=200, alpha=0.5)
#
#
#
#
#
#
#
#
# # kmeans = KMeans(n_clusters = 30, init ='k-means++')
# # kmeans.fit(X[X.columns[1:3]]) # Compute k-means clustering.
# # X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])
# # centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
# # labels = kmeans.predict(X[X.columns[1:3]])
# # X.head(10)
#
# # X.plot.scatter(x = 'latitude', y = 'longitude', c=labels, s=50, cmap='viridis')
# # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
#
#
# ###########################################################
#
# # f = pd.read_csv('skootel coordinate files')    #Read the dataframe file to get points with coordinate position
# # df.head(20)                                     #and give me the top 20 coordinates in the list
#
#
# # Randomly chose k examples as initial centroids from dataframe   #In our case we can do 30 as a naive count
#
# # Elbow Curve Chart algorithm               #With Elbow Curve algorithm we can see the actual number of k we
#                                             #need for the right amount of clusters
#
#
# # while not null:                               #While longitude and latitude not null
#   #  create k clusters by assigning each    #This will choose random points from data frame and make them into k
#    #     example to closest centroid        #ammount of centroids
#                                             #The closest points will change to the color closest to the centroid
#
#     # compute k new centroids by averaging  #Code will re-iterate the K-means algorithm until Elbow Curve chart
#       #  examples in each cluster          #changes are minimal.
#
#    # if centroids dont change:             #If centroids do not change after a while of re-iterating
#     #    break                             #finish code and print chart plot; K variable is found.
#
#
# # while not null:
#   #  create k (Known value) clusters by assigning each   #Now that K is known, iterate until k ammount
#    #     example to closes centroid
#
#     # plot cluster chart