import matplotlib.pyplot as plt
from scipy.spatial import distance


def KNN_test(X_train, Y_train, X_test, Y_test, K):
    k_labels = []
    results = []
    for i, test_point in enumerate(X_test):
        calculated_dist = {}
        for j, train_point in enumerate(X_train):
            dist = round(distance.euclidean(test_point, train_point), 2)
            calculated_dist[j] = [dist, Y_train[j], train_point]
        k_dist = sorted(calculated_dist, key=lambda x: calculated_dist[x][0])[:K]
        k_labels.append(1 if sum([calculated_dist[dist][1] for dist in k_dist]) > 0 else -1)
        results.append(1 if (k_labels[-1] > 0 and Y_test[i] > 0) or (k_labels[-1] < 0 and Y_test[i] < 0) else 0)

    # Plotting data points
    # if len(X_train[0]) == 2:
    #     x_values = [val for val in X_train[:, 0]]
    #     y_values = [val for val in X_train[:, 1]]
    #     # Plot train data
    #     fig = plt.figure()
    #     fig.suptitle("KNN with K = " + str(K))
    #     plt.subplot(1, 3, 1)
    #     plot_points(x_values, y_values, Y_train, "Train")
    #
    #     # Plot test data
    #     x_values = [val for val in X_test[:, 0]]
    #     y_values = [val for val in X_test[:, 1]]
    #     plt.subplot(1, 3, 2)
    #     plot_points(x_values, y_values, Y_test, "Test")
    #
    #     # Plot predicted data
    #     plt.subplot(1, 3, 3)
    #     plot_points(x_values, y_values, k_labels, "Predicted")
    #     plt.show()
    return sum(results) / len(results)


def choose_K(X_train, Y_train, X_val, Y_val):
    k_labels = []
    results = []
    k_results = [0, 0]  # [ accuracy , k ]
    for curr_k in range(3, len(X_train), 2):
        for i, test_point in enumerate(X_val):
            calculated_dist = {}
            for j, train_point in enumerate(X_train):
                dist = round(distance.euclidean(test_point, train_point), 2)
                calculated_dist[j] = [dist, Y_train[j], train_point]
            k_dist = sorted(calculated_dist, key=lambda x: calculated_dist[x][0])[:curr_k]
            k_labels.append(1 if sum([calculated_dist[dist][1] for dist in k_dist]) > 0 else -1)
            results.append(1 if (k_labels[-1] > 0 and Y_val[i] > 0) or (k_labels[-1] < 0 and Y_val[i] < 0) else 0)
        accuracy = sum(results) / len(results)
        if accuracy > k_results[0]:
            k_results = [accuracy, curr_k]
    return k_results[1]


def plot_points(x_values, y_values, labels, title):
    plt.title(title)
    if title != "Test":
        x_pos_vals = [x_val for i, x_val in enumerate(x_values) if labels[i] == 1]
        y_pos_vals = [y_val for i, y_val in enumerate(y_values) if labels[i] == 1]
        x_neg_vals = [x_val for i, x_val in enumerate(x_values) if labels[i] == -1]
        y_neg_vals = [y_val for i, y_val in enumerate(y_values) if labels[i] == -1]
        plt.plot(x_pos_vals, y_pos_vals, '+')
        plt.plot(x_neg_vals, y_neg_vals, '_')
    else:
        plt.plot(x_values, y_values, 'ro')
