import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import csv




class Clusters:
        # DF is the data from the rides
        def __init__(self,df, clust = 12):

                self.df = df
                self.clust = clust
                start="new_start"
                end="new_end"


                self.slat = start+"_lat" #slat = "new_start_lat"
                self.slong = start+"_long" #slat = "new_start_long"
                self.elat = end+"_lat" #elat = "new_end_lat"
                self.elong = end+"_long" #elat = "new_end_long"

        def createCluster(self,output='./Output/PrepoCluster.csv'):
                # latitude=self.target+"lat"
                #
                # longitude = self.target+"long"
                # self.df = self.df[self.df[latitude] >= 17].reset_index(drop=True)  # Remove invalid coordinates
                # self.df.dropna(axis = 0, how = 'any', subset=[latitude, longitude], inplace = True)
                # X=self.df[:,[latitude,longitude]]
                # print(X)
                Xstart= self.df[[self.slat,self.slong]]

                self.kmeansStart = KMeans(n_clusters=self.clust).fit(Xstart)
                self.df['start_cluster'] = self.kmeansStart.labels_.astype(int)
                # print(df['start_cluster'])

                Xend= self.df[[self.elat,self.elong]]


                self.kmeansEnd = KMeans(n_clusters=self.clust).fit(Xend)
                self.df['end_cluster'] = self.kmeansEnd.labels_.astype(int)

                ####################################################################

                # DF for Concatenated Lats and Longs

                lats1 = self.df[self.slat]
                lats2 = self.df[self.elat]
                lats = pd.concat([lats1,lats2])

                long1 =  self.df[self.slong]
                long2 =  self.df[self.elong]
                long = pd.concat([long1,long2])

                # Create DF with both lats and longs
                #lol
                newdf = {}
                newdf["lat"] = lats
                newdf["long"] = long

                newdf = pd.DataFrame(newdf)

                halflength = len(self.df[self.slat])



                # Create Labels DF
                labels1 = KMeans(n_clusters=self.clust).fit(newdf)
                labels = labels1.labels_.astype(int)

                self.df['start_cluster'] = labels[0:halflength]
                self.df['end_cluster'] = labels[halflength:]

                print(self.df)


                # print(labels)
                # print(len(labels))
                # longs = [self.df[[self.slong, self.elong]]]

                # print(newdf)
                # print(len(newdf)) #mitad = 63,816

                # newdf['lat'] = pd.concat[lats[self]]
                # newdf['long'] = longs
                # print(newdf)
                # print(self.df)

                self.df.to_csv(output)
                return self.df




        # def plotCluster(self):
        #         """
        #                Use ./Output/PreprocessedIntervals.csv as your df (when initializing object)
        #
        #                 Create cluster labels using the new_ (start,long) _lat andnew_ (start,long) _long. [3,4,0,....1,9]
        #                 Do it for both start and end coordinates
        #                 Create column:
        #                         self.df['cluster_start'] =  cluster labels of start
        #                         self.df['cluster_end'] =  cluster labels of end
        #                         self.df.to_csv('./Output/nombredecsv.csv')
        #                 return self.df
        #
        #
        #
        #         """
        #
        #
        #         self.createCluster()
        #         plt.scatter(self.df[self.longitude], self.df[self.latitude], c = self.kmeans.labels_.astype(float),s=50, alpha=0.5)
        #         plt.scatter(self.centroids[:, 1], self.centroids[:, 0], c = 'red', s=50)
        #         plt.show()




# df = pd.read_csv('./Output/PreprocessedIntervals.csv')

# tool = Clusters(df)
# # tool.createCluster()
# tool.plotCluster()
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