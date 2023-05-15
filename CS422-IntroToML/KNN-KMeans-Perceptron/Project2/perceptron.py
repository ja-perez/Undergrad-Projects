import numpy as np
import matplotlib.pyplot as plt


def perceptron_train(X, Y):
    update_flag = 0
    weight, bias = np.zeros(len(X[0])), 0
    while True:
        for sample_i, sample in enumerate(X):
            activation_pairs = list(zip(sample, weight))
            pair_sums = sum([pair[0] * pair[1] for pair in activation_pairs])
            sample_activation = pair_sums + bias
            if sample_activation * Y[sample_i] <= 0:
                update_flag = 1
                bias += Y[sample_i]
                for weight_i, _ in enumerate(weight):
                    weight[weight_i] += sample[weight_i] * Y[sample_i]
        if update_flag:
            update_flag = 0
        else:
            break

    # Plotting decision boundary

    # x_values = [val for val in X[:, 0]]
    # y_values = [val for val in X[:, 1]]
    # plot_points(x_values, y_values, Y, "Train")
    #
    # # weight : [x, y]
    # # bias : b
    # # 0 = w[0] * x + w[1] * y + b
    # # y = - (w[0] / w[1]) * x - (b / w[1])
    # x_lower, x_upper = min(x_values) - 1, max(x_values) + 1
    # y_lower, y_upper = min(y_values) - 1, max(y_values) + 1
    # x_vals = np.array([x_lower, x_upper])
    # y_db_lower = (-1 * (weight[0] / weight[1]) * x_lower) - (bias / weight[1])
    # y_db_upper = (-1 * (weight[0] / weight[1]) * x_upper) - (bias / weight[1])
    # y_vals = np.array([y_db_lower, y_db_upper])
    # plot_points(x_vals, y_vals, title="Decision Boundary")
    #
    # plt.axis([x_lower, x_upper, y_lower, y_upper])
    # plt.show()
    return weight, bias


def perceptron_test(X_test, Y_test, w, b):
    outcomes = []
    for i, curr_x in enumerate(X_test):
        result = sum([curr_x[x_i] * w[x_i] for x_i, _ in enumerate(curr_x)]) + b
        outcomes.append(1 if result * Y_test[i] > 0 else 0)
    return round(sum(outcomes) / len(outcomes), 2)


def plot_points(x_values, y_values, labels=None, title=""):
    plt.title(title)
    if title != "Decision Boundary":
        x_pos_vals = [x_val for i, x_val in enumerate(x_values) if labels[i] == 1]
        y_pos_vals = [y_val for i, y_val in enumerate(y_values) if labels[i] == 1]
        x_neg_vals = [x_val for i, x_val in enumerate(x_values) if labels[i] == -1]
        y_neg_vals = [y_val for i, y_val in enumerate(y_values) if labels[i] == -1]
        plt.plot(x_pos_vals, y_pos_vals, '+')
        plt.plot(x_neg_vals, y_neg_vals, '_')
    else:
        plt.plot(x_values, y_values, '--')
