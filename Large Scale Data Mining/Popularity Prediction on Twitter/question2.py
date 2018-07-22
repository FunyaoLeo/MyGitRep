#!/usr/bin/python

from os.path import join
from tqdm import tqdm
import json

from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer    
from nltk.tokenize.regexp import RegexpTokenizer
import numpy as np

from sklearn import svm
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_curve
import sklearn.metrics as metrics
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

import re
import string
import random
import math
import matplotlib.pyplot as plt


#online source
def is_in_wa(location):
	true_list = [
		"washington",
		"seattle",
		"kirkland",
		"wa"
	]

	false_list = [
		"dc",
		"d.c."
	]

	flag = False
	location = location.split()


	for s in false_list:
		if s in location:
			flag = False
			return flag
			
	for s in true_list:
		if s in location:
			flag = True
			return flag

	return flag

def is_in_mas(location):
	true_list = [
		"massachusetts",
		"ma",
		"boston",
		"northampton",
		"springfield",
		"plymouth",
		"arlington",
		"scituate",
		"worcester"
	]

	location = location.split()

	false_list = [
		"ohio",
	]
	flag = False

	for s in false_list:
		if s in location:
			flag = False
			return flag
				
	for s in true_list:
		if s in location:
			flag = True
			return flag

	return flag
		
ver=2#2-snowball 1-lancanster else-porter

class tokenizer(object):
	def __init__(self):
		self.tokenize=RegexpTokenizer(r'\b([A-Za-z]+)\b') #remove the punctuations
		if ver==2:
			self.stemmer = SnowballStemmer("english")         #using stemmed version of words
		elif ver==1:
			self.stemmer = LancasterStemmer()	
		else:
			self.stemmer = PorterStemmer()
	def __call__(self, doc):
		return [self.stemmer.stem(token) for token in self.tokenize.tokenize(doc)]

stop_words=text.ENGLISH_STOP_WORDS
def get_vectorizer():
	return CountVectorizer(
		tokenizer=tokenizer(),
		lowercase=True,
		min_df = 2,
		max_df = 0.99,
		stop_words=stop_words
	)

def get_tfid_transformer():
	return TfidfTransformer(
		norm='l2',
		sublinear_tf=True
	)

def get_svd():
	return TruncatedSVD(n_components=100)

def plot_figure(actual, predicted, classifier_name):
	plt.figure()
	x_data, y_data, threshold = roc_curve(actual, predicted)
	plt.plot(x_data, y_data, label="ROC Curve")
	plt.plot([0, 1], [0, 1])

	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.2])

	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('ROC Curves for ' + classifier_name + 'Classifier')
	plt.legend(loc="best")

def get_performance(actual, predicted):
	print("The accuracy is ", metrics.accuracy_score(actual, predicted))
	print("The precision is ", metrics.precision_score(actual, predicted, average='macro'))
	print("The recall is ", metrics.recall_score(actual, predicted, average='macro'))
	print("The confusion matrix is ")
	print(metrics.confusion_matrix(actual, predicted))

def classify(data, label, classifier, cname):
	#use 90% data to train, and the rest 15% are used to do test
	index = math.floor(0.9 * data.shape[0])
	index = int(index)
	train_data = data[:index,:]
	train_label = label[:index]

	test_data = data[index:, :]
	test_label = label[index:]

	classifier.fit(train_data, train_label)
	predicted = classifier.predict(test_data)
	predicted_probs = classifier.predict_proba(test_data)
	
	print("Performance of "+cname+" classifier:")
	get_performance(test_label, predicted)
	plot_figure(test_label, predicted_probs[:, 1], cname)

print("Loading tweets about superbowl")
lcount = 1348767
foldname = 'tweet_data'
filename = 'tweets_#superbowl.txt'

with open(join(foldname, filename), 'r') as tweet_file:
	data = []
	label = []
	for i, line in tqdm(enumerate(tweet_file), total=lcount):
		tweet_data = json.loads(line)
		location = tweet_data.get("tweet").get("user").get("location").lower()

		if is_in_wa(location):
			data.append(tweet_data.get("title"))
			label.append(0)
		elif is_in_mas(location):
			data.append(tweet_data.get("title"))
			label.append(1)

	pipe = Pipeline(
		[
			('vectorize', get_vectorizer()),
			('tf-idf', get_tfid_transformer()),
			('svd', get_svd())
		]
	)

	data = pipe.fit_transform(data)
	label = np.array(label)

	indexes = range(data.shape[0])
	random.shuffle(indexes)
	indexes = indexes
	select_data = data[indexes, :]
	select_label = label[indexes]

	svm_classifier = svm.SVC(kernel='linear', probability=True)
	random_classifier = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
	MLP_classifier = MLPClassifier(alpha=1)
	classify(select_data, select_label, svm_classifier, "SVM")
	classify(select_data, select_label, AdaBoostClassifier(), "AdaBoost")
	classify(select_data, select_label, random_classifier, "RandomForest")
	classify(select_data, select_label, MLP_classifier, "Neural Network ")
	
	plt.show()
