import math
from sklearn import tree


def get_train_error(weights, y_hat, y):
    weighted_errors = [weight * (y[i] != y_hat[i]) for i, weight in enumerate(weights)]
    return sum(weighted_errors)


def compute_alpha(e_hat):
    return 0.5 * math.log((1 - e_hat) / e_hat, math.e)


def update_weights(weights, a, y_hat, y):
    z_vals = {}
    for i, weight in enumerate(weights):
        re_weight = weight * math.exp(-1 * a * y[i] * y_hat[i])
        weights[i] = re_weight
        if re_weight not in z_vals:
            z_vals[re_weight] = 1
        else:
            z_vals[re_weight] += 1
    z = sum([z_vals[weight] * weight for weight in z_vals])
    for i, _ in enumerate(weights):
        weights[i] *= (1 / z)
    return weights


def apply_weights(x, y, weights):
    new_x, new_y = [], []
    # Calculate new dataset len with duplicates
    unique_weights = list(set(weights))
    weight_mult = 1.0 / unique_weights[0]
    weight_mult = int(math.ceil(weight_mult)) if weight_mult - int(weight_mult) >= 0.5 else int(math.floor(weight_mult))
    for weight in unique_weights[1:]:
        w_denom = 1.0 / weight
        if w_denom - int(w_denom) >= 0.5:
            w_denom = int(math.ceil(w_denom))
        else:
            w_denom = int(math.floor(w_denom))
        weight_mult = math.lcm(weight_mult, w_denom)

    for i, data in enumerate(x):
        data_mult = int(weights[i] * weight_mult)
        for _ in range(data_mult):
            new_x.append(data)
            new_y.append(y[i])
    return new_x, new_y


def adaboost_train(X, Y, max_iter):
    weights = [1 / len(X) for _ in X]  # [1/12 1/12 1/12 ... 1/12]
    alphas = []
    trained_classifiers = []
    for _ in range(max_iter):
        weighted_X, weighted_Y = apply_weights(X, Y, weights)
        tree_stump = tree.DecisionTreeClassifier(max_depth=1)
        tree_stump.fit(weighted_X, weighted_Y)
        trained_classifiers.append(tree_stump)
        y_hat = tree_stump.predict(X, Y)
        e_hat = get_train_error(weights, y_hat, Y)
        alpha = compute_alpha(e_hat)
        alphas.append(alpha)
        weights = update_weights(weights, alpha, y_hat, Y)
    return trained_classifiers, alphas


def adaboost_test(X, Y, f, alpha):
    votes = [0 for _ in X]
    for i, classifier in enumerate(f):
        vote = classifier.predict(X)                    # Prediction of decision tree f(i) on data set X
        weighted_vote = alpha[i] * vote                 # Applying weight(alpha) to f(i) prediction
        for j, _ in enumerate(votes):
            votes[j] += weighted_vote[j]                # Taking sum of each data points index to calculate sign
    votes = [1 if vote > 0 else -1 for vote in votes]   # Calculating prediction of each data point using signs
    outcomes = []
    for i, vote in enumerate(votes):
        outcomes.append(1 if vote == Y[i] else 0)       # Calculating amount of correct predictions against Y values
    return sum(outcomes) * 1.0 / len(outcomes)          # Calculating accuracy of predictions using number of correct
                                                        # predictions / total predictions
