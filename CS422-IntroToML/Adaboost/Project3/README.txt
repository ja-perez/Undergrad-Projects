Javier Perez
11/09/2022
CS 422
Project 3 Report

Write-up 1:
    Due to the nature of updating, calculating, and applying weights to every sample
    in our data set, having a decision tree stump allows us to increase the efficiency
    in which we process each tree. Training a decision tree with depth > 1 will add a
    significant amount of processing time and power that will only marginally increase
    the accuracy of the model, thus using stumps makes the most sense.

    This differentiates adaboost from a random forest ensemble due to the random forest
    ensemble accepting decision trees of larger depth however they are not trained to
    improve features, rather to be representative of a random sample of the entire data set.
    Adaboost on the other hand derives its functionality from taking a data set and continually
    training various (or the same) classifiers on an improved classification of that data set
    and its features.

Write-up 2:
    To run an adaboost algorithm with a perceptron rather than a decision tree first we would
    have to change our classifiers to a perceptron then we would have to take into consideration
    the updating of the weights and bias hyperparameters per classifier training, other than
    that, the rest of the steps will be exactly the same.