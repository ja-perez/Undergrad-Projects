import numpy as np
import matplotlib.pyplot as plt


def compute_covariance_matrix(Z):
    z_cov = np.matmul(Z.T, Z)
    return z_cov


def find_pcs(cov):
    pcs = np.linalg.eig(cov)
    return pcs


def project_data(Z, PCS, L):
    max_eig = np.argmax(PCS)
    eig_norm = np.linalg.norm(L[max_eig])
    max_vals = L[max_eig] / eig_norm
    z_projected = np.matmul(Z, max_vals)
    return z_projected


def show_plot(Z, Z_star):
    plt.title('Principle Component Analysis')

    Z_x, Z_y = Z[:, 0], Z[:, 1]
    plt.plot(Z_x, Z_y, 'ro')
    Z_sx, Z_sy = Z_star, np.zeros(Z_star.shape)
    plt.plot(Z_sx, Z_sy, marker='o')

    plt.show()
