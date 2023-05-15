import helpers
import pandas as pd


def get_tags(data):
    tags = {}
    for i, entry in enumerate(data[:-1]):
        tag = entry[1]
        next_tag = data[i + 1][1]
        if tag == '</s>':
            continue
        elif tag not in tags:
            tags[tag] = {'count': 1, 'next_tags': {next_tag: 1}}
        else:
            tags[tag]['count'] += 1
            if next_tag not in tags[tag]['next_tags']:
                tags[tag]['next_tags'][next_tag] = 1
            else:
                tags[tag]['next_tags'][next_tag] += 1
    return tags


def gen_transition_table(data, tags):
    entries = {}
    for tag in tags:
        entries[tag] = {}
        for next_tag in tags:
            if tag == next_tag:
                pass

    table = 0
    return table


def train_hmm(train_data):
    tags = get_tags(train_data)
    words = {}

    transition_table, emission_table = [], []
    # transition_table = gen_transition_table(train_data, tags)

    # for sentence in train_data:
    #     for entry in sentence:
    #         tag = entry[1]
    #         if tag not in tags:
    #             tags[tag] = {"count": 1, 'words': {}}
    #         else:
    #             tags[tag]["count"] += 1
    #
    # words = {}
    # # loop through each sentence and calculate the bigrams
    # for sentence in train_data:
    #     for i, entry in enumerate(sentence[:-1]):
    #         tag = sentence[i + 1][1]
    #         given_tag = entry[1]
    #         word = entry[0]
    #         if tag not in tags[given_tag]:
    #             tags[given_tag][tag] = 1
    #         else:
    #             tags[given_tag][tag] += 1
    #         if i != 0:
    #             if word not in words and word != '</s>':
    #                 words[word] = 1
    #             elif word != '</s>':
    #                 words[word] += 1
    #             if word not in tags[given_tag]['words']:
    #                 tags[given_tag]['words'][word] = 1
    #             else:
    #                 tags[given_tag]['words'][word] += 1
    #
    # transition_table = [[tag for tag in tags if tag != '<s>' and tag != '</s>']]
    # probabilities = []
    # # calculate the bigram probabilities for each tag pair and create the table
    # for given_tag in tags:
    #     bigram = [given_tag]
    #     for tag in transition_table[0]:
    #         if tag not in tags[given_tag]:
    #             bigram_counts = 0
    #         else:
    #             bigram_counts = tags[given_tag][tag]
    #         prob = bigram_counts / tags[given_tag]['count']
    #         bigram.append(prob)
    #     probabilities.append(bigram)
    # transition_table.extend(probabilities)
    #
    # # emission table
    # emission_table = [[word for word in words]]
    # emission_tags = [tag for tag in tags if tag != '<s>' and tag != '</s>']
    # for tag in emission_tags:
    #     emission_probs = [tag]
    #     for word in words:
    #         if word not in tags[tag]['words']:
    #             word_count = 0
    #         else:
    #             word_count = tags[tag]['words'][word]
    #         prob = word_count / tags[tag]['count']
    #         emission_probs.append(prob)
    #     emission_table.append(emission_probs)
    return transition_table, emission_table


def test_hmm(test_data, hmm_transition, hmm_emission):
    return 0, [0] * 10


def main():
    t_data = helpers.load_pos_data("pos_test.txt")
    train_hmm(t_data)


if __name__ == '__main__':
    main()
