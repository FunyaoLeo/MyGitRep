EE236 - Project part i


Project Title

Multiclassification Problem

Introduction
This project implements a second norm and soft margin SVM classifier from theory. Then it implemnts
"one vs one" (ovo) and “one vs rest” (ovr) algorithm and employs them seperately on digit number
dataset. The dataset has been preprocessed using PCA. The highest accuracy could reach 0.9045.

How to use()
1 make sure zipped file is unzipped and all the files are in the same folder. Open multiclas-
  sification and do the following changes.

2 load your data in %%%% load data %%%% part. 
  Some things to mention: First, make sure the label is a number larger than 0. If it is not,
			  please bias the minimum label to 1. (As in the sample code, S_Train
			  is 0~9, so I add 1 to bias them to 1~10.)
			  Second, Please make sure that your feature matrix is of the format
			  "number of features X data points", the label vector is of the
			  format "number of data points X 1"
3 (optional) if you are still using MNIST data set, you can use %%%% dimension reduction %%%%
  to do the dimension reduction. Change the "for index" loop to any data points you want to
  do dimension reduction. If you are not using MNIST data, then please leace the comment as it
  is
4 In %creating two classifiers part, crease two classifiers. MyClassifier1 is "one vs one" algorithm
  MyClassifier2 is "one vs rest". First variable in MyClassifier is number of lables. Second is
  dimension of features.
5 In %train and classify part, change the variable in train method and classify method to any thing you
  want to test
6 run the code, hit1 represents how many testing points are correctly classified in "ovo" algorithm and 
  hit2 represnets points in "ovr" algorithm.

Author

Fangyao Liu----UCLA ECE Graduate student
	       UID:204945018
	       Email:fangyao@okstate.edu