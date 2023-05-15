from sklearn.model_selection import train_test_split
from helpers import load_data, clean_data
from doc2vec import train_doc2vec, tokenize_dataset
from performance import train, test

# example: "./twitter_sentiment_data.csv"
fname = input("Please input the path to the dataset: ")

documents, labels = load_data(fname)

cleaned_documents, cleaned_labels = clean_data(documents, labels)

d2v_model = train_doc2vec(cleaned_documents)

vectorized_cleaned_documents = tokenize_dataset(cleaned_documents, d2v_model)

X_train, X_test, y_train, y_test = train_test_split(vectorized_cleaned_documents, cleaned_labels, test_size=0.33, random_state=1, stratify=cleaned_labels)

trained_models_dict = train(X_train, y_train)

model_performance_metric_dict = test(trained_models_dict, X_test, y_test)

for dict_key in model_performance_metric_dict.keys():
    print(f"{dict_key}: {model_performance_metric_dict[dict_key]}")
