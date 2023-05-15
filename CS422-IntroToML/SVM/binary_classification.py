import numpy as np
import matplotlib as plt
import helpers as h


def svm_train_brute(training_data):
    return 0, 0, 0


def distance_point_to_hyperplane(pt, w, b):
    pass


def compute_margin(data, w, b):
    pass


def svm_test_brute(w, b, x):
    pass


def main():
    training_data = h.generate_training_data_binary(1)
    [w, b, S] = svm_train_brute(training_data)


if __name__ == '__main__':
    main()
