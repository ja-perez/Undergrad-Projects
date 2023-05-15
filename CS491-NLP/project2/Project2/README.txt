Javier Perez
CS 491 - Project 2
04-11-2023

Helper Functions:
Preprocessing of pos_data includes removing words using the average counts for the upper half and lower half
ranges of the overall average. The starting tag '<s>' and ending tag '</s>' were also included to
facilitate the division between sentences in constructing the HMM transition tables. The words were also
processed in lowercase in order to limit the amount of repeated words, this was taken into consideration
when designing the testing functions.

Preprocessing of the spam/ham data also included the removal of words using the average counts for the
upper half and lower half ranges of the overall average. The words were also processed in lowercase in
order to limit the amount of repeated words, this was taken into consideration when designing the testing
functions.
