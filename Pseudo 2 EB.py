import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()

# 5 datapoints with 3 features
df = pd.read_csv('./ride_data/HullEx.csv')
df = df[df['Latitude'] >= 17].reset_index(drop=True)  # Remove invalid coordinates
df.dropna(axis = 0, how = 'any', subset=['Latitude', 'Longitude'], inplace = True)
Y=df.loc[:,['Latitude','Longitude']]
print(Y)

# data = [[1, 0, 0],
#         [1, 0.2, 0],
#         [0, 0, 1],
#         [0, 0, 0.9],
#         [1, 0, 0.1]]

X = np.array(Y)

distance_matrix(X,X)

centroid_idx = [0,2] # let data point 0 and 2 be our centroids
centroids = X[centroid_idx,:]
print(centroids)

kmeans = KMeans(n_clusters=2, init=centroids) # just run one k-Means iteration so that the centroids are not updated

kmeans.fit(X)
kmeans.labels_
plt.scatter(centroids[:, 1], centroids[:, 0], c = 'red', s=50)
# plt.plot()
plt.show()