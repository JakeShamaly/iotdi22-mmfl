Jake Shamaly & Evan Raftery
ECE 535
Federated Learning Project

This folder contains mostly code provided by the original paper. However, some modifications (as logged on our GitHub repository) have been made.

The main change to make note of here is the addition of analysis_v2.py. This is our personal analysis file that only runs analysis on the opp dataset. The reasoning for this is that, in order to generate result.txt files for all tests on all 3 datasets (opp, mHealth, URFall), we would have to run nearly 100 tests. Given that my laptop does not have CUDA, these tests can take anywhere from 20-30 minutes all the way up to an hour to complete. Hence, we simply have commented out the other 2 datasets. We also remove the "N_REPS" variable, as this would require the tests to run multiple times with different seeds (64, to be exact...), which is also far too much testing for the same time constraint reason as before. The main major addition in the analysis_v2.py file is that of the per_class_statistics() method, which takes in per class statistics from results.txt and outputs them into a bar graph.

The per-class statistics used to create the graphs in per_class_statistics() are calculated in the eval() function in server.py, which now returns these statistics to be appended to the results.txt file (which is done in fl.py).