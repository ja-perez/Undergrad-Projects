from os import getcwd, path, listdir
from random import shuffle


def avg_counts(word_counts: {str: int}):
    total_counts = sum([word_counts[word] for word in word_counts])
    total_words = len(word_counts)
    return total_counts // total_words


def get_uncommon_words(word_counts: {str: int}):
    overall_avg = avg_counts(word_counts)
    upper_half = {word: word_counts[word] for word in word_counts if word_counts[word] > overall_avg}
    upper_half_avg = avg_counts(upper_half)
    lower_half = {word: word_counts[word] for word in word_counts if word_counts[word] <= overall_avg}
    lower_half_avg = avg_counts(lower_half)
    uncommon_avg = (overall_avg + lower_half_avg) // 2
    uncommon_words = [word for word in word_counts if
                      word_counts[word] <= uncommon_avg or word_counts[word] >= upper_half_avg]
    return uncommon_words


def get_word_counts(fname):
    try:
        word_counts = {}
        with open(fname) as file:
            for line in file:
                line = line.split()
                try:
                    word = line[0].lower()
                    if word not in word_counts:
                        word_counts[word] = 1
                    else:
                        word_counts[word] += 1
                except IndexError as _:
                    pass
        return word_counts
    except FileNotFoundError as _:
        error_msg = "!Error: " + fname + " does not exist in working directory(" \
                    + getcwd() + ")."
        print(error_msg)


def load_pos_data(fname):
    start_tag, end_tag = ['', '<s>'], ['', '</s>']
    data = [start_tag]
    try:
        with open(fname) as file:
            word_counts = get_word_counts(fname)
            uncommon_words = get_uncommon_words(word_counts)
            for line in file:
                line = line.split()
                if not line:
                    data.append(start_tag)
                else:
                    word = line[0].lower()
                    if word == '.':
                        data.append(end_tag)
                        continue
                    elif word not in uncommon_words:
                        entry = [word, line[1]]
                        data.append(entry)
        return data
    except FileNotFoundError as _:
        error_msg = "!Error: " + fname + " does not exist in working directory(" \
                    + getcwd() + ")."
        print(error_msg)
    return data


def get_vocab(dirname):
    ham_dir_path = path.join(dirname, 'ham')
    spam_dir_path = path.join(dirname, 'spam')
    paths = [ham_dir_path, spam_dir_path]
    vocab = {}
    for dir_path in paths:
        files = listdir(dir_path)
        for file in files:
            file_path = path.join(dir_path, file)
            with open(file_path, 'r') as f:
                try:
                    for line in f:
                        words = [word for word in line.split() if word]
                        for word in words:
                            word = word.lower()
                            if word not in vocab:
                                vocab[word] = 1
                            else:
                                vocab[word] += 1
                except UnicodeDecodeError as _:
                    # File encoded incorrectly, pass for now
                    pass
    return vocab


def load_spam_data(dirname):
    """ 80% Train 20% Test """
    ham_dir_path = path.join(dirname, 'ham')
    spam_dir_path = path.join(dirname, 'spam')
    paths = {'ham': ham_dir_path, 'spam': spam_dir_path}

    data = {"ham": [], "spam": []}

    vocab_counts = get_vocab(dirname)
    uncommon_vocab = get_uncommon_words(vocab_counts)
    vocab = {word: vocab_counts[word] for word in vocab_counts if word not in uncommon_vocab}

    for file_class in paths:
        dir_path = paths[file_class]
        files = listdir(dir_path)
        for file in files:
            file_path = path.join(dir_path, file)
            with open(file_path, 'r') as f:
                bag_of_words = {word: 0 for word in vocab}
                try:
                    for line in f:
                        words = [word for word in line.split() if word]
                        for word in words:
                            word = word.lower()
                            if word in bag_of_words:
                                bag_of_words[word] += 1
                except UnicodeDecodeError as _:
                    # File encoded incorrectly, pass for now
                    pass
            data[file_class].append(bag_of_words)

    shuffle(data['ham'])
    shuffle(data['spam'])
    train_ham_total, train_spam_total = int(.8 * len(data['ham'])), int(.8 * len(data['spam']))
    test_ham_total, test_spam_total = 1 - train_ham_total, 1 - train_spam_total
    train_data = {'ham': data['ham'][:train_ham_total], 'spam': data['spam'][:train_spam_total]}
    test_data = {'ham': data['ham'][:test_ham_total], 'spam': data['spam'][:test_spam_total]}
    return train_data, test_data


def main():
    pos_data = load_pos_data("pos_test.txt")
    print(pos_data)
    enron_data = load_spam_data("enron1")


if __name__ == '__main__':
    main()
