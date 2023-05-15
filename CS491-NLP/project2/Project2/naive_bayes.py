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


def train_naive_bayes(train_data):
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
    nb_model = {data_class: {} for data_class in train_data}
    total_files = sum([len(train_data[file_class]) for file_class in train_data])

    for data_class in train_data:
        # Class probability
        nb_model[data_class]['prob'] = len(train_data[data_class]) / total_files
        files_bows = train_data[data_class]
        word_counts = get_word_counts(files_bows)
        total_words = sum([word_counts[x] for x in word_counts])
        vocab = sum([1 for _ in word_counts])
        for word in word_counts:
            count = word_counts[word]
            nb_model[data_class][word] = (count + 1) / (total_words + vocab)

    return nb_model


def test_naive_bayes(test_data, model):
    """
    test_data: {  class_type0 : [
                                    { 'word in bag of words' : # of word in file, ... }
                                            ...
                                ],
                  class_type1 : [
                                    { 'word in bag of words' : # of word in file, ... }
                                            ...
                                ],
                  ...
                }
    model : {   class_type0: {
                                class_type0_prob: prob,
                                word0_prob: prob0,
                                word1_prob: prob1,
                                ...
                             },
                class_type1: {
                                class_type0_prob: prob,
                                word0_prob: prob0,
                                word1_prob: prob1,
                                ...
                             }
            }
    """
    prediction_result = []

    for class_label in test_data:
        for sample in test_data[class_label]:
            predictions = {}
            for data_class in model:
                # P(sample) = P(class)
                class_prob = model[data_class]['prob']
                predictions[data_class] = class_prob
                # P(sample) = P(class) * P(word0) * P(word1) * ...
                for word in sample:
                    word = word.lower()
                    if word not in model[data_class]:
                        word_prob = 1
                    else:
                        word_prob = model[data_class][word] ** sample[word]
                    predictions[data_class] *= word_prob
            predicted_class = max(predictions, key=predictions.get)

            if predicted_class != class_label:
                prediction_result.append(0)
            else:
                prediction_result.append(1)
    return sum(prediction_result) / len(prediction_result)


def main():
    # data = {'pos': [{'good': 3, 'poor': 0, 'great': 3}, {'good': 0, 'poor': 1, 'great': 2}],
    #         'neg': [{'good': 1, 'poor': 3, 'great': 0}, {'good': 1, 'poor': 5, 'great': 2},
    #                 {'good': 0, 'poor': 2, 'great': 0}]
    #         }
    # data1 = {'pos': [{'good': 2, 'poor': 1, 'great': 1}]
    #          }
    train, test = load_spam_data('enron1')
    model = train_naive_bayes(train)
    acc = test_naive_bayes(test, model)
    print(acc)


if __name__ == '__main__':
    main()
