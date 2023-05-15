import numpy as np
import matplotlib.pyplot as plt
import PCA as pca

test_data_1 = np.array([[1, 2], [-4, 3], [0, 0], [-8, -2], [3, 1],
                        [9, -2], [-11, -3], [-18, 3], [-15, 0], [-13, 1],
                        [-8, 1], [-2, -3], [-4, -1], [-19, -2], [20, 1],
                        [14, 3], [11, -3], [7, -2], [15, 0], [12, -3]])
test_data_2 = np.array([[1, 4], [-6, -8], [3, 3], [-15, -11], [5, 1],
                        [-6, -3], [0, 4], [-13, -10], [-2, 1], [-9, -8],
                        [-9, -11], [8, 6], [2, -2], [0, 0], [12, 13],
                        [10, 8], [6, 10], [-3, -5], [-1, -1], [-4, -9]])

# PCA video dataset
test_data_3 = np.array([[1, 1], [1, 0], [2, 2], [2, 1],
                        [2, 4], [3, 4], [3, 3], [3, 2],
                        [4, 4], [4, 5], [5, 5], [5, 7], [5, 4]])

Z = test_data_2
cov = pca.compute_covariance_matrix(Z)
pcs, L = pca.find_pcs(cov)
Z_star = pca.project_data(Z, pcs, L)
pca.show_plot(Z, Z_star)
