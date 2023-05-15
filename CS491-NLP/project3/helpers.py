import time
from os import makedirs
from os.path import join, exists
import re


def load_data(fname):
    """
    Loads data from file.
    """
    docs, labels = [], []
    with open(fname) as file:
        for i, line in enumerate(file):
            line = line.strip("\n")
            values = line.split('","')
            docs.append(values[-1])
            labels.append(values[0])
    return docs, labels


def clean_data(docs, labels):
    """
    Updates labels with 0 for negative sentiment and 1 for positive sentiment.
    Removes links, @mentions, and punctuation marks (# , : ; etc.).
    """
    clean_docs, clean_labels = [], []
    for i, content in enumerate(docs):
        label = labels[i].strip("\'\"")
        # lower case
        content = content.lower()
        # remove links
        content = re.sub(r"http\S+", "", content)
        # remove @mentions
        content = re.sub(r"@\S+", "", content)
        # remove punctuation marks
        content = re.sub("['\"#!?:;.,-]", "", content)
        if not validate_data(content, label):
            docs.pop(i)
            labels.pop(i)
            continue
        # replace label 4 with 1
        label = "1" if label == "4" else "0"

        clean_docs.append(content)
        clean_labels.append(label)

    return clean_docs, clean_labels


def validate_data(content, label):
    """
    Validates data checking that a valid label and content are present.
    """
    try:
        assert (label in ("0", "4", "1"))
        assert (content != "" and content != " ")
        return True
    except AssertionError:
        return False


""" Utils to avoid re-loading and cleaning data while debugging """
def load_clean_data(fname):
    """
    Loads cleaned data from file if it exists,
    otherwise loads raw data from file, cleans it, stores it to file and then loads it.
    """
    cleaned_data_id = "cleaned_data.csv"
    gen_data_dir = "generated_data"
    cleaned_data_path = join(gen_data_dir, cleaned_data_id)
    if exists(cleaned_data_path):
        print("Loading saved cleaned data...")
        cleaned_documents, cleaned_labels = load_data(cleaned_data_path)
        print("Clean data loaded.")
    else:
        print("Loading raw data from file...")
        load_start = time.time()
        documents, labels = load_data(fname)
        load_end = time.time()
        print("Data loaded in {:.2f} seconds.".format(load_end - load_start), end="\n\n")
        print("Cleaning data...")
        clean_start = time.time()
        cleaned_documents, cleaned_labels = clean_data(documents, labels)
        clean_end = time.time()
        print("Data cleaned in {:.2f} seconds.".format(clean_end - clean_start), end="\n\n")
        makedirs(gen_data_dir, exist_ok=True)
        print("Storing cleaned data to file...")
        store_clean_data(cleaned_documents, cleaned_labels, cleaned_data_path)
        print("Data stored.")
    return cleaned_documents, cleaned_labels


def store_clean_data(clean_docs, clean_labels, fname):
    """
    Stores cleaned data to file for future loading.
    """
    with open(fname, "w") as file:
        for i, doc in enumerate(clean_docs):
            file.write(f"{clean_labels[i]}\",\"{doc}\n")


def main():
    data_id = "twitter_sentiment_data"
    data_file = '.'.join([data_id, "csv"])
    data_path = join(data_id, data_file)
    clean_docs, clean_labels = load_clean_data(data_path)
    # documents, labels = load_data(data_path)
    # clean_docs, clean_labels = clean_data(documents, labels)
    pass  # breakpoint


if __name__ == '__main__':
    main()
