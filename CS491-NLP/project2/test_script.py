import helpers
import hmm
import naive_bayes as nb
import logistic_regression as lr

# Test HMM
train_data = helpers.load_pos_data("pos_train.txt")
test_data = helpers.load_pos_data("pos_test.txt")

hmm_transition, hmm_emission = hmm.train_hmm(train_data)
acc, seq_acc = hmm.test_hmm(test_data, hmm_transition, hmm_emission)
print("HMM:", acc)
print(seq_acc[:10])  # Check the accuracy of the first 10 sequences

# Test Naive Bayes
train_data, test_data = helpers.load_spam_data("enron1")
model = nb.train_naive_bayes(train_data)
acc = nb.test_naive_bayes(test_data, model)
print("Naive Bayes:", acc)

# Test Logistic Regression
# Use same train and test from naive bayes
model = lr.train_logistic_regression(train_data)
acc = lr.test_logistic_regression(test_data, model)
print("Logistic Regression:", acc)
