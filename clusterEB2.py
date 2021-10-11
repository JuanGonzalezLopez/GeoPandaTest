from sklearn.cluster import KMeans
import numpy as np

x1 = [[1],[1],[2],[2],[2],[3],[3],[7],[7],[7]]
x2 = [[1],[1],[2],[2],[2],[3],[3],[7],[7],[7]]

X_2D = np.concatenate((x1,x2),axis=1)

kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
labels = kmeans.fit(X_2D)

print(labels.labels_)