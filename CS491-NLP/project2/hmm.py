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


def get_tag_words(data):
    tag_words = {}
    all_words = set()
    for i, entry in enumerate(data):
        word = entry[0]
        tag = entry[1]
        if not word:
            continue
        if tag not in tag_words:
            tag_words[tag] = {'count': 1, word: 1}
        else:
            tag_words[tag]['count'] += 1
            if word not in tag_words[tag]:
                tag_words[tag][word] = 1
            else:
                tag_words[tag][word] += 1
        all_words.add(word)
    return all_words, tag_words


def gen_transition_table(tags):
    all_tags = [tag for tag in tags]
    entries = {}
    for given_tag in tags:
        entries[given_tag] = {}
        for next_tag in all_tags:
            if given_tag == '<s>' and next_tag == '<s>':
                continue
            if next_tag in tags[given_tag]['next_tags']:
                next_counts = tags[given_tag]['next_tags'][next_tag]
                given_count = tags[given_tag]['count']
                entries[given_tag][next_tag] = next_counts / given_count
            else:
                entries[given_tag][next_tag] = 0
    return entries


def gen_emission_table(all_words, tag_words):
    entries = {}
    for tag in tag_words:
        entries[tag] = {}
        for word in all_words:
            if word in tag_words[tag]:
                given_tag = tag_words[tag][word]
                tag_count = tag_words[tag]['count']
                entries[tag][word] = given_tag / tag_count
            else:
                entries[tag][word] = 0
    return entries


def train_hmm(train_data):
    tags = get_tags(train_data)
    all_words, tag_words = get_tag_words(train_data)

    transition_table = gen_transition_table(tags)
    emission_table = gen_emission_table(all_words, tag_words)

    return transition_table, emission_table


def test_hmm(test_data, hmm_transition, hmm_emission):
    prediction_results = []
    deltas, prev_state, prev_word = [], '', ''
    word_prob, state_prob = 1, 1
    for value in test_data:
        word = value[0]
        tag = value[1]
        if tag == '<s>':
            prev_state = tag
            word_prob = 1
            deltas = [1] * len(hmm_transition)
        for state in hmm_transition:
            pass

    return 0, [0] * 10


def main():
    t_data = helpers.load_pos_data("pos_test.txt")
    transition, emission = train_hmm(t_data)
    test_hmm(t_data, transition, emission)


if __name__ == '__main__':
    main()
