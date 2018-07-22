import json
import os
import math
import pytz
import datetime
import numpy as np
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

data_path="./tweets"
min_data = 1000000000
max_data = 0
time_dict_aggregate = {}

for file_name in os.listdir(data_path):

    if file_name.endswith(".txt"):
        with open(os.path.join(data_path, file_name)) as text:
            print file_name
            for i, line in enumerate(text):
                json_object = json.loads(line)

                time = json_object['firstpost_date']
                pst_tz = pytz.timezone('US/Pacific')
                time = datetime.datetime.fromtimestamp(time, pst_tz)
                time_count = (time.month-1)*31*24+(time.day-1)*24+time.hour


                #aggregate

                if time_count not in time_dict_aggregate:
                    time_dict_aggregate.setdefault(time_count, [0, 0, 0, 0, 0, 0, 0, 0])
                if time_count in time_dict_aggregate:
                    time_dict_aggregate[time_count][0] += 1  # number of tweets
                    time_dict_aggregate[time_count][1] += json_object['tweet']['user'][
                        'favourites_count']  # number_of_favorite_accounts
                    if json_object['tweet']['user']['favourites_count'] > time_dict_aggregate[time_count][2]:  # max of favorite accounts
                        time_dict_aggregate[time_count][2] = json_object['tweet']['user']['favourites_count']
                    time_dict_aggregate[time_count][3] += json_object['tweet']['user']['friends_count']  # number of friends
                    time_dict_aggregate[time_count][4] += json_object['metrics']['ranking_score']  # number of ranking score
                    time_dict_aggregate[time_count][5] += json_object['metrics']['citations']['total']  # number of retweets
                    time_dict_aggregate[time_count][6] += json_object['author']['followers']  # number of followers

print "aggregate file:"
time_range = [key for key, value in time_dict_aggregate.iteritems()]
del time_range[0:5]

feature = [value for key, value in time_dict_aggregate.iteritems()]
new_feature = []
for index in range(len(feature)-5):
    new_feature_tmp = []
    for subindex in range(5):
        new_feature_tmp += feature[index+subindex]
    new_feature.append(new_feature_tmp)
feature = new_feature

label = [value[0] for key, value in time_dict_aggregate.iteritems()]
del label[0:5]

# the first begining to 02/01/8:00
print "the first begining to 02/01/8:00"
superbowl_start = time_range.index(752)
label_before = np.array(label[0:superbowl_start])
feature_before = np.array(feature[0:superbowl_start])


# Linear Regression
lr1 = linear_model.LinearRegression()
lr1.fit(feature_before, label_before)


# 02/01/8:00 to 8:00 PM
print "02/01/8:00 to 8:00 PM"
superbowl_start = time_range.index(752)
superbowl_end = time_range.index(764)
label_before = np.array(label[superbowl_start:superbowl_end])
feature_before = np.array(feature[superbowl_start:superbowl_end])


# Logistic Regression
logimodel2 = linear_model.LogisticRegression()
logimodel2.fit(feature_before, label_before)


# 02/01/8:00 PM to end
print "02/01/8:00 PM to end"
superbowl_end = time_range.index(765)
label_before = np.array(label[superbowl_end:])
feature_before = np.array(feature[superbowl_end:])

# Linear Regression
lr3 = linear_model.LinearRegression()
lr3.fit(feature_before, label_before)


data_path_2 = "./tests"
for file_name in os.listdir(data_path_2):
    time_sample_dict = {}
    feature_sample = []
    label_sample = []
    if file_name.endswith(".txt"):
        with open(os.path.join(data_path_2, file_name)) as text:
            print file_name
            for i, line in enumerate(text):
                json_object=json.loads(line)
                time = json_object['firstpost_date']
                pst_tz=pytz.timezone('US/Pacific')
                time=datetime.datetime.fromtimestamp(time, pst_tz)
                time_count = (time.month-1)*31*24+(time.day-1)*24+time.hour

                if time_count not in time_sample_dict:
                    time_sample_dict.setdefault(time_count, [0, 0, 0, 0, 0, 0, 0, 0])
                if time_count in time_sample_dict:
                    time_sample_dict[time_count][0] += 1  # number of tweets
                    time_sample_dict[time_count][1] += json_object['tweet']['user']['favourites_count']  # number_of_favorite_accounts
                    if json_object['tweet']['user']['favourites_count'] > time_sample_dict[time_count][2]:  # max of favorite accounts
                        time_sample_dict[time_count][2] = json_object['tweet']['user']['favourites_count']
                    time_sample_dict[time_count][3] += json_object['tweet']['user']['friends_count']  # number of friends
                    time_sample_dict[time_count][4] += json_object['metrics']['ranking_score']  # number of ranking score
                    time_sample_dict[time_count][5] += json_object['metrics']['citations']['total']  # number of retweets
                    time_sample_dict[time_count][6] += json_object['author']['followers']  # number of followers

            time_range = [key for key, value in time_sample_dict.iteritems()]
            del time_range[0:5]

            feature = [value for key, value in time_sample_dict.iteritems()]

            new_feature = []
            for index in range(len(feature) - 5):
                new_feature_tmp = []
                for subindex in range(5):
                    new_feature_tmp += feature[index + subindex]

            feature = [new_feature_tmp]

            label = [value[0] for key, value in time_sample_dict.iteritems()]
            print label
            del label[0:5]
            test_predict1 = lr1.predict(feature)
            test_predict2 = logimodel2.predict(feature)
            test_predict3 = lr3.predict(feature)

            print "period 1 prediction = "
            print test_predict1
            print "real value"
            print  label
            print "period 2 prediction = "
            print test_predict2
            print "real value"
            print  label
            print "period 3 prediction = "
            print test_predict3
            print "real value"
            print  label