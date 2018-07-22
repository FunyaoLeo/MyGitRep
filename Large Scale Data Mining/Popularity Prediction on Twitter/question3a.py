from statsmodels.regression.linear_model import OLS
from statsmodels.api import add_constant
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
import numpy as np
import json,os
import math
import datetime
import random
import pytz
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.metrics import roc_curve
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import accuracy_score

def plot_figure(actual, predicted):
    plt.figure()
    x_data, y_data, threshold = roc_curve(actual, predicted)
    plt.plot(x_data, y_data, label="ROC Curve")
    plt.plot([0, 1], [0, 1])
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.2])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves for Logistic Regression')
    plt.show()




data_path="./tweet_data"
min_data = 1000000000
max_data = 0
for file_name in os.listdir(data_path):
    number_of_tweets = 0
    number_of_retweets = 0
    number_of_followers = 0
    time_dict={}
    feature=[]
    label=[]
    max_time=0
    min_time=100000000
    follower_list=[]
    retweet_list=[]
    if file_name.endswith(".txt"):
        with open(os.path.join(data_path,file_name)) as text:
            print file_name

            for i,line in enumerate(text):
                json_object=json.loads(line)
                follower_list.append([json_object['author']['followers'],json_object['tweet']['user']['friends_count'],json_object['tweet']['user']['favourites_count']])
                retweet_list.append(json_object['metrics']['citations']['total'])

    back_retweet_list=list(retweet_list)
    for i in range(len(retweet_list)):
        if retweet_list[i]>1:
            retweet_list[i]=1
        else:
            retweet_list[i]=0
    x_train,x_test,y_train,y_test=train_test_split(np.array(follower_list),np.array(retweet_list) ,test_size=0.2,random_state=42)
    lr=linear_model.LogisticRegression()
    lr.fit(x_train,y_train)
    test_predict = lr.predict(x_test)
    print "for logistic regression model accuracy = % f" %(accuracy_score(y_test, test_predict))
    count1=0
    count2=0
    new_follower_list = []
    new_retweet_list = []
    for i in range(len(back_retweet_list)):
        if back_retweet_list[i]>=5:
            back_retweet_list[i]=1
            count1+=1
        else:
            back_retweet_list[i] = 0
            count2+=1
    for i in range(len(back_retweet_list)):
        if back_retweet_list[i]==1:
            new_follower_list.append(follower_list[i])
            new_retweet_list.append(1)
        else:
            if random.random()<0.01:
                new_follower_list.append(follower_list[i])
                new_retweet_list.append(0)


    x_train, x_test, y_train, y_test = train_test_split(np.array(new_follower_list), np.array(new_retweet_list), test_size=0.2, random_state=42)
    lr = linear_model.LogisticRegression()
    lr.fit(x_train, y_train)
    test_predict = lr.predict(x_test)
    predicted_probs = lr.predict_proba(x_test)

    plot_figure(y_test, predicted_probs[:,1])
    print "to predict hot tweets accuracy = % f" % (accuracy_score(y_test, test_predict))







