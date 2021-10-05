import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import csv

class Clusters:
        # DF is the data from the rides
        def __init__(self, df, clust = 12):
                self.df = df
                self.clust = clust
        # Create DataFrame
        def createCluster(self):
                df = pd.read_csv('./ride_data/HullEx.csv')
                df = df[df['Latitude'] >= 17].reset_index(drop=True)  # Remove invalid coordinates
                self.df.dropna(axis = 0, how = 'any', subset=['Latitude', 'Longitude'], inplace = True)
                X=self.df.loc[:,['Latitude','Longitude']]
                print(X)
                self.kmeans = KMeans(n_clusters=self.clust).fit(df)
                self.centroids = self.kmeans.cluster_centers_
                print(self.kmeans)
                print(self.centroids)


        def plotCluster(self):
                self.createCluster()
                plt.scatter(self.df['Longitude'], self.df['Latitude'], c = self.kmeans.labels_.astype(float),s=50, alpha=0.5)
                plt.scatter(self.centroids[:, 1], self.centroids[:, 0], c = 'red', s=50)
                plt.show()

                # Elbow Curve: 12 Clusters
                # K_clusters = range(1,100)
                # kmeans = [KMeans(n_clusters=i) for i in K_clusters]
                # y_axis = df[['Latitude']]
                # x_axis = df[['Longitude']]
                # score = [kmeans[i].fit(y_axis).score(y_axis) for i in range(len(kmeans))]
                #
                # plt.plot(K_clusters, score)
                # plt.xlabel('Numero de Clusters')
                # plt.ylabel('Score')
                # plt.title('Elbow Curve')
                # plt.show()


                ###################################################

                # Code to manually add the centroids

                # data = [[18.2036534554253,-67.1432842412368],
                #         [18.21090066197647,-67.140327357859],
                #         [18.2143185762837,-67.1449586699717],
                #         [18.2156944274901,-67.1476364135741],
                #         [18.20834467867308,-67.14036502661509],
                #         [18.21396222131919,-67.14547342452374],
                #         [18.21087121410492,-67.13953130870321],
                #         [18.21116007930294,-67.14133848752897],
                #         [18.21698746774393,-67.1424664925079],
                #         [18.21255278220406,-67.14108760783827]]
                # points = np.array(data)
                # distance_matrix(points, points)
                # centroid_idx = [0,1,2,3,4,5,6,7,8,9]
                # centroids = points[centroid_idx,:]
                #####################################################


                ###############################################








                # kmeans = KMeans(n_clusters = 30, init ='k-means++')
                # kmeans.fit(X[X.columns[1:3]]) # Compute k-means clustering.
                # X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])
                # centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
                # labels = kmeans.predict(X[X.columns[1:3]])
                # X.head(10)

                # X.plot.scatter(x = 'latitude', y = 'longitude', c=labels, s=50, cmap='viridis')
                # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)


                ###########################################################

                # f = pd.read_csv('skootel coordinate files')    #Read the dataframe file to get points with coordinate position
                # df.head(20)                                     #and give me the top 20 coordinates in the list


                # Randomly chose k examples as initial centroids from dataframe   #In our case we can do 30 as a naive count

                # Elbow Curve Chart algorithm               #With Elbow Curve algorithm we can see the actual number of k we
                                                            #need for the right amount of clusters


                # while not null:                               #While longitude and latitude not null
                  #  create k clusters by assigning each    #This will choose random points from data frame and make them into k
                   #     example to closest centroid        #ammount of centroids
                                                            #The closest points will change to the color closest to the centroid

                    # compute k new centroids by averaging  #Code will re-iterate the K-means algorithm until Elbow Curve chart
                      #  examples in each cluster          #changes are minimal.

                   # if centroids dont change:             #If centroids do not change after a while of re-iterating
                    #    break                             #finish code and print chart plot; K variable is found.


                # while not null:
                  #  create k (Known value) clusters by assigning each   #Now that K is known, iterate until k ammount
                   #     example to closes centroid

                    # plot cluster chart
                    # #Print cluster chart containing point and clusters