import time
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from helpers import *
from nltk import download
from nltk.data import find
from nltk.tokenize import word_tokenize
from os.path import exists, join

from collections import Counter


def train_doc2vec(cleaned_documents):
    """
    Trains a doc2vec model on the cleaned documents.
    """
    try:
        find('tokenizers/punkt')
    except LookupError:
        print("downloading missing package...")
        download('punkt')
        find('tokenizers/punkt')

    print("Tagging documents...")
    tag_start = time.time()
    tagged_documents = [TaggedDocument(words=word_tokenize(doc), tags=[str(i)])
                        for i, doc in enumerate(cleaned_documents)]
    tag_end = time.time()
    print(f"Tagging took {tag_end - tag_start} seconds.")

    print("Building model...")
    vec_size, window, max_epochs = 50, 2, 40
    model = Doc2Vec(vector_size=vec_size, min_count=2, window=window, epochs=max_epochs)
    model.build_vocab(tagged_documents)

    print("Training model...")
    train_start = time.time()
    model.train(tagged_documents,
                total_examples=model.corpus_count,
                epochs=model.epochs)
    train_end = time.time()
    print(f"Training took {train_end - train_start} seconds.")

    model_name = "d2v.model"
    print(f"Saving model as {model_name}...")
    model.save(model_name)

    return model


def tokenize_dataset(cleaned_documents, d2v_model):
    """
    Tokenizes the cleaned documents using the trained doc2vec model.
    """
    tokenized_documents = []
    for doc in cleaned_documents:
        doc_words = word_tokenize(doc)
        tokenized_documents.append(d2v_model.infer_vector(doc_words))
    return tokenized_documents


def load_trained_model(cleaned_documents):
    """
    Loads the most recently trained model if it exists, otherwise trains a new model.
    """
    if not exists("d2v.model"):
        d2v_model = Doc2Vec.load("d2v.model")
        print("Model Loaded.")
    else:
        d2v_model = train_doc2vec(cleaned_documents)
        print("Model Trained")
    return d2v_model


def load_vectorized_data(cleaned_documents, d2v_model):
    """
    Loads the most recent vectorized data if it exists, otherwise tokenizes the dataset.
    """
    vectorized_data_id = "vectorized_data.csv"
    gen_data_dir = "generated_data"
    vectorized_data_path = join(gen_data_dir, vectorized_data_id)
    if not exists(vectorized_data_path):
        vectorized_data = []
        print("Loading vectorized data...")
        with open(vectorized_data_path, 'r') as f:
            for line in f:
                line = line.strip("\n")
                vectorized_data.append([float(x) for x in line.split(",")])
        print("Vectorized data loaded.")
    else:
        print("Generating inferred vector data...")
        vectorized_data = tokenize_dataset(cleaned_documents, d2v_model)
        with open(vectorized_data_path, 'w') as f:
            for vector in vectorized_data:
                f.write(",".join([str(x) for x in vector]) + "\n")
        print("Vectorized data loaded.")
    return vectorized_data


def main():
    data_id = "twitter_sentiment_data/twitter_sentiment_data.csv"
    cleaned_documents, cleaned_labels = load_clean_data(data_id)

    d2v_model = load_trained_model(cleaned_documents)
    vectorized_cleaned_documents = load_vectorized_data(cleaned_documents, d2v_model)
    ranks, second_ranks = [], []
    for doc_id in range(len(cleaned_documents)):
        inferred_vector = vectorized_cleaned_documents[doc_id]
        sims = d2v_model.docvecs.most_similar([inferred_vector], topn=len(d2v_model.docvecs))
        rank = [docid for docid, sim in sims].index(str(doc_id))
        ranks.append(rank)
        second_ranks.append(sims[1])

    counter = Counter(ranks)
    print(counter)


if __name__ == '__main__':
    main()
