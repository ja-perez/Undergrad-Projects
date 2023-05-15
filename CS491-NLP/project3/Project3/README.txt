Javier Perez
Project 3
5/4/23

This program was written and tested in Python 3.11.0 on Windows 11.

The functions were split up into 3 files:
    - helpers.py
        - load_data
        - clean_data
    - doc2vec.py
        - train_doc2vec
        - tokenize_dataset
    - performance.py
        - train
        - test

* Note:
I read lines from the text file directly, as opposed to using
something like the pandas library read_csv method, due to an error with the encoding of the
text file, despite using other encoding methods. When testing this direct method
on google colab the same error occurred, however it has not occurred when
testing locally so results may vary.

Data Preprocessing:
Per the assignment instructions, labels with a 0, 4 were replaced with a 0, 1, respectively.
The data was read using a split of '","' to avoid splitting tweets with ',' unnecessarily.
In preprocessing the data, certain characters and words were removed.
This includes:
    - punctuation marks (e.g. !, ?, ., etc.)
    - links (e.g. https://...)
    - mentions (e.g. @some_user)
With the removal of these characters, some tweets were left empty.
These tweets were removed from the dataset as well.

Training Doc2Vec:
First the cleaned document was tagged with the index of the tweet.
The tagged documents were then used to train the Doc2Vec model.
The parameters used to train the Doc2Vec model include:
    - vector size: 50
    - window size: 2
    - min count: 2
    - epochs: 40
Tagging the cleaned documents took approximately 105 secs. or 1 minute and 45 secs.
Training the Doc2Vec model took approximately 2410 secs. or 40 minutes and 10 secs.

* Note:
- Various helpers methods were used while developing the program that would save
and load previous results to avoid having to re-run the entire program. These methods
may have impacted the results of future model training and testing.