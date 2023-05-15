from sklearn.metrics import f1_score, balanced_accuracy_score
from helpers import load_clean_data
from doc2vec import load_trained_model, load_vectorized_data
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron


def train(X_train, y_train):
    """
    Trains a decision tree and perceptron model on the training data and returns a dictionary of trained models
    """
    trained_models_dict = {}

    # Decision Tree
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    trained_models_dict["decision_tree_classifier"] = dt

    # Perceptron
    perceptron = Perceptron()
    perceptron.fit(X_train, y_train)
    trained_models_dict["perception_classifier"] = perceptron

    return trained_models_dict


def test(trained_models_dict, x_test, y_test):
    """
    Tests trained models on test data and returns a dictionary of model performance metrics
    """
    model_performance_metrics = {}
    for model in trained_models_dict:
        key_acc = '_'.join([model, "accuracy"])
        key_bal_acc = '_'.join([model, "balanced_accuracy"])
        key_f1 = '_'.join([model, "f1"])
        val_acc = trained_models_dict[model].score(x_test, y_test)
        val_bal_acc = balanced_accuracy_score(y_test, trained_models_dict[model].predict(x_test))
        val_f1 = f1_score(y_test, trained_models_dict[model].predict(x_test), average='macro')

        model_performance_metrics[key_acc] = val_acc
        model_performance_metrics[key_bal_acc] = val_bal_acc
        model_performance_metrics[key_f1] = val_f1

    return model_performance_metrics


def main():
    data_id = "twitter_sentiment_data/twitter_sentiment_data.csv"
    cleaned_documents, cleaned_labels = load_clean_data(data_id)
    d2v_model = load_trained_model(cleaned_documents)
    vectorized_cleaned_documents = load_vectorized_data(cleaned_documents, d2v_model)

    x_train, x_test, y_train, y_test = train_test_split(
        vectorized_cleaned_documents, cleaned_labels,
        test_size=0.33, random_state=1, stratify=cleaned_labels)

    trained_models_dict = train(x_train, y_train)
    model_performance_metric_dict = test(trained_models_dict, x_test, y_test)

    print()
    for dict_key in model_performance_metric_dict.keys():
        print(f"{dict_key}: {model_performance_metric_dict[dict_key]}")


if __name__ == '__main__':
    main()
