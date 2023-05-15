import numpy as np
from scipy.spatial import distance


def K_Means(X, K, mu):
    if not mu.any():
        rng = np.random.default_rng()
        mu = rng.choice(X, replace=False)
    elif np.ndim(X) != np.ndim(mu):
        pass
    elif len(X[0]) != len(mu[0]):
        rng = np.random.default_rng()
        mu = rng.choice(X, K, replace=False)
    elif len(mu) < K:
        rng = np.random.default_rng()
        for _ in range(K - len(mu)):
            additional_clusters = np.array([rng.choice(X, replace=False)])
            mu = np.append(mu, additional_clusters, axis=0)
    epoch = 1
    prev_mu = np.copy(mu)
    while True:
        cluster_distances = {cluster_i: [] for cluster_i, _ in enumerate(mu[:])}
        for point in X:
            curr_distances = {}
            for cluster_i, cluster_center in enumerate(mu[:]):
                if np.ndim(X) == 1:
                    point_cluster_distance = round(distance.euclidean([point], cluster_center), 2)
                else:
                    point_cluster_distance = round(distance.euclidean(point, cluster_center), 2)
                curr_distances[cluster_i] = point_cluster_distance
            closest_cluster_i = sorted(curr_distances, key=lambda x: curr_distances[x])[0]
            cluster_distances[closest_cluster_i].append(point)
        for indices in cluster_distances:
            cluster_points = cluster_distances[indices]
            new_cluster = sum(cluster_points) / len(cluster_points)
            mu[indices] = new_cluster
        if np.array_equal(prev_mu, mu):
            # print(epoch)
            break
        epoch += 1
        prev_mu = np.copy(mu)
    return mu


# 622
def K_Means_better(X, K):
    pass
