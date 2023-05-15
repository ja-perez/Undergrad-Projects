from math import exp, log

from helpers import load_spam_data


def get_word_counts(bag_list):
    words = {}
    for bag in bag_list:
        for word in bag:
            if word not in words:
                words[word] = bag[word]
            else:
                words[word] += bag[word]
    return words


def get_gradients(y, z, x):
    dw = {word: x[word] * (z - y) for word in x}
    db = z - y
    return dw, db


def train_logistic_regression(train_data):
    """
    train_data: {
                  class_type0 : [
                                    { 'word in bag of words' : # of word in file, ... }
                                            ...
                                ],
                  class_type1 : [
                                    { 'word in bag of words' : # of word in file, ... }
                                            ...
                                ],
                  ...
                }
    """
    vocab = len(train_data['ham'][0])
    w, b = {word: 1 / vocab for word in train_data['ham'][0]}, 0
    labels = {'ham': 1, 'spam': 0}
    learning_rate = 0.2
    epochs = 5
    for epoch in range(epochs):
        for data_class in train_data:
            y = labels[data_class]
            for sample in train_data[data_class]:
                z = sum([w[word] * sample[word] for word in sample]) + b
                try:
                    sig = 1 / (1 + exp(-1 * z))
                except OverflowError as _:
                    sig = 0
                # loss = -1 * (y * log(sig) + (1 - y) * log(1 - sig))
                dw, db = get_gradients(y, sig, sample)
                w = {word: w[word] - learning_rate * dw[word] for word in dw}
                b = b - learning_rate * db

    return {'weights': w, 'bias': b}


def test_logistic_regression(test_data, model):
    labels = {'ham': 1, 'spam': 0}
    results = []
    for data_class in test_data:
        y = labels[data_class]
        for sample in test_data[data_class]:
            y_hat = sum([sample[word.lower()] * model['weights'][word.lower()] for word in sample]) + model['bias']
            y_hat = 1 if y_hat > 0.5 else 0
            results.append(1 if y_hat == y else 0)
    return sum(results) / len(results)


def main():
    # data = {'pos': [{'good': 3, 'poor': 0, 'great': 3}, {'good': 0, 'poor': 1, 'great': 2}],
    #         'neg': [{'good': 1, 'poor': 3, 'great': 0}, {'good': 1, 'poor': 5, 'great': 2},
    #                 {'good': 0, 'poor': 2, 'great': 0}]
    #         }
    train, test = load_spam_data('enron1')
    model = train_logistic_regression(train)
    acc = test_logistic_regression(test, model)
    print(acc)


if __name__ == '__main__':
    main()
