import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import distance_matrix

# 5 datapoints with 3 features
data = [[1, 0, 0],
        [1, 0.2, 0],
        [0, 0, 1],
        [0, 0, 0.9],
        [1, 0, 0.1]]

X = np.array(data)

distance_matrix(X,X)

centroid_idx = [0,2] # let data point 0 and 2 be our centroids
centroids = X[centroid_idx,:]
print(centroids) # [[1. 0. 0.]
                 # [0. 0. 1.]]

kmeans = KMeans(n_clusters=2, init=centroids, max_iter=1) # just run one k-Means iteration so that the centroids are not updated

kmeans.fit(X)
kmeans.labels_