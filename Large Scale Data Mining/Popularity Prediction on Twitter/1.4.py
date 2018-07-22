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
import matplotlib.pyplot as plt

data_path = "./tweets"


min_data = 1000000000
max_data = 0
time_dict_aggregate = {}

for file_name in os.listdir(data_path):

    time_dict = {}
    feature = []
    label = []
    max_time = 0
    min_time = 100000000

    if file_name.endswith(".txt"):
        with open(os.path.join(data_path, file_name)) as text:
            print file_name
            for i, line in enumerate(text):
                json_object = json.loads(line)

                time = json_object['citation_date']
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



                # selected features for GO_Hawks, Go_Patriots, Patriots, Superbowl
                if file_name == 'tweets_#gohawks.txt' or file_name == 'tweets_#gopatriots.txt' or file_name == 'tweets_#patriots.txt' or file_name == 'tweets_#superbowl.txt':
                    if max_time < time_count:
                        max_time = time_count
                    if min_time > time_count:
                        min_time = time_count
                    if time_count not in time_dict:
                        time_dict.setdefault(time_count, [0, 0, 0, 0, 0, 0, 0, 0])
                    if time_count in time_dict:
                        time_dict[time_count][0] += 1                                          # number of tweets
                        time_dict[time_count][1] += json_object['tweet']['user']['favourites_count']  # number_of_favorite_accounts
                        if json_object['tweet']['user']['favourites_count'] > time_dict[time_count][2]:  # max of favorite accounts
                            time_dict[time_count][2] = json_object['tweet']['user']['favourites_count']
                        time_dict[time_count][3] += json_object['tweet']['user']['friends_count']     # number of friends
                        time_dict[time_count][4] += json_object['metrics']['ranking_score']           # number of ranking score
                        time_dict[time_count][5] += json_object['metrics']['citations']['total']      # number of retweets
                        time_dict[time_count][6] += json_object['author']['followers']                #number of followers

                # selected features for nfl
                elif file_name == 'tweets_#nfl.txt':
                    if max_time < time_count:
                        max_time = time_count
                    if min_time > time_count:
                        min_time = time_count
                    if time_count not in time_dict:
                        time_dict.setdefault(time_count, [0, 0, 0, 0, 0, 0, 0])
                        time_dict[time_count][3] = time.hour
                    if time_count in time_dict:
                        time_dict[time_count][0] += 1                    # number of tweets
                        time_dict[time_count][1] += json_object['metrics']['ranking_score']  # ranking score
                        time_dict[time_count][2] += json_object['tweet']['user']['friends_count']  # number of friends
                        time_dict[time_count][4] += json_object['tweet']['user']['favourites_count']  # number_of_favorite_accounts
                        time_dict[time_count][5] += json_object['metrics']['citations']['total']  # number of retweets
                        time_dict[time_count][6] += json_object['author']['followers']  # number of followers

                # selected features for sb49
                elif file_name == 'tweets_#sb49.txt':
                    if max_time < time_count:
                        max_time = time_count
                    if min_time > time_count:
                        min_time = time_count
                    if time_count not in time_dict:
                        time_dict.setdefault(time_count, [0, 0, 0, 0, 0, 0, 0])
                    if time_count in time_dict:
                        time_dict[time_count][0] += 1                    # number of tweets
                        time_dict[time_count][1] += json_object['metrics']['ranking_score']  # ranking score
                        if json_object['tweet']['user']['favourites_count'] > time_dict[time_count][2]:  # max of favorite accounts
                            time_dict[time_count][2] = json_object['tweet']['user']['favourites_count']
                        time_dict[time_count][3] += json_object['tweet']['user']['friends_count']  # number of friends
                        time_dict[time_count][4] += json_object['tweet']['user']['favourites_count']  # number_of_favorite_accounts
                        time_dict[time_count][5] += json_object['metrics']['citations']['total']  # number of retweets
                        time_dict[time_count][6] += json_object['author']['followers']  # number of followers


        time_range = [key for key, value in time_dict.iteritems()]
        del time_range[len(time_range)-1]

        feature = [value for key, value in time_dict.iteritems()]
        del feature[len(feature)-1]

        label = [value[0] for key, value in time_dict.iteritems()]
        del label[0]




        # first is the first begining to 02/01/8:00
        print "the first begining to 02/01/8:00"
        superbowl_start = time_range.index(752)
        label_before = np.array(label[0:superbowl_start])
        feature_before = np.array(feature[0:superbowl_start])

        lrerror = 0
        polyerror = 0
        logierror = 0

        kf = KFold(n_splits=10, shuffle=True)
        for train_index, test_index in kf.split(feature_before):
            features_train, labels_train = feature_before[train_index], label_before[train_index]
            features_test, labels_test = feature_before[test_index], label_before[test_index]
            # Linear Regression
            lr = linear_model.LinearRegression()
            lr.fit(features_train, labels_train)
            test_predict = lr.predict(features_test)
            lrerror += math.sqrt(mean_squared_error(test_predict, labels_test))


            # Polynomial Regression
            poly = PolynomialFeatures(2)
            polymodel = linear_model.LinearRegression()
            polymodel.fit(poly.fit_transform(features_train), labels_train)
            test_predict = polymodel.predict(poly.fit_transform(features_test))
            polyerror += math.sqrt(mean_squared_error(test_predict, labels_test))

            # Logistic Regression
            logimodel = linear_model.LogisticRegression()
            logimodel.fit(features_train, labels_train)
            test_predict = logimodel.predict(features_test)
            logierror += math.sqrt(abs(mean_squared_error(test_predict, labels_test)))
        print 'linear regression model error: ' + str(lrerror/10.0)
        print 'polynomial mode error: ' + str(polyerror/10.0)
        print 'logistic mode error: ' + str(logierror/10.0)

        # 02/01/8:00 to 8:00 PM
        print "02/01/8:00 to 8:00 PM"
        superbowl_start = time_range.index(752)
        superbowl_end = time_range.index(764)
        label_before = np.array(label[superbowl_start:superbowl_end])
        feature_before = np.array(feature[superbowl_start:superbowl_end])

        lrerror = 0
        polyerror = 0
        logierror = 0

        kf = KFold(n_splits=10, shuffle=True)
        for train_index, test_index in kf.split(feature_before):
            features_train, labels_train = feature_before[train_index], label_before[train_index]
            features_test, labels_test = feature_before[test_index], label_before[test_index]
            # Linear Regression
            lr = linear_model.LinearRegression()
            lr.fit(features_train, labels_train)
            test_predict = lr.predict(features_test)
            lrerror += math.sqrt(mean_squared_error(test_predict, labels_test))

            # Polynomial Regression
            poly = PolynomialFeatures(2)
            polymodel = linear_model.LinearRegression()
            polymodel.fit(poly.fit_transform(features_train), labels_train)
            test_predict = polymodel.predict(poly.fit_transform(features_test))
            polyerror += math.sqrt(mean_squared_error(test_predict, labels_test))

            # Logistic Regression
            logimodel = linear_model.LogisticRegression()
            logimodel.fit(features_train, labels_train)
            test_predict = logimodel.predict(features_test)
            logierror += math.sqrt(abs(mean_squared_error(test_predict, labels_test)))
        print 'linear regression model error: ' + str(lrerror / 10.0)
        print 'polynomial mode error: ' + str(polyerror / 10.0)
        print 'logistic mode error: ' + str(logierror / 10.0)

        # 02/01/8:00 PM to end
        print "02/01/8:00 PM to end"
        superbowl_end = time_range.index(765)
        label_before = np.array(label[superbowl_end:])
        feature_before = np.array(feature[superbowl_end:])

        lrerror = 0
        polyerror = 0
        logierror = 0

        kf = KFold(n_splits=10, shuffle=True)
        for train_index, test_index in kf.split(feature_before):
            features_train, labels_train = feature_before[train_index], label_before[train_index]
            features_test, labels_test = feature_before[test_index], label_before[test_index]
            # Linear Regression
            lr = linear_model.LinearRegression()
            lr.fit(features_train, labels_train)
            test_predict = lr.predict(features_test)
            lrerror += math.sqrt(mean_squared_error(test_predict, labels_test))

            # Polynomial Regression
            poly = PolynomialFeatures(2)
            polymodel = linear_model.LinearRegression()
            polymodel.fit(poly.fit_transform(features_train), labels_train)
            test_predict = polymodel.predict(poly.fit_transform(features_test))
            polyerror += math.sqrt(mean_squared_error(test_predict, labels_test))

            # Logistic Regression
            logimodel = linear_model.LogisticRegression()
            logimodel.fit(features_train, labels_train)
            test_predict = logimodel.predict(features_test)
            logierror += math.sqrt(abs(mean_squared_error(test_predict, labels_test)))
        print 'linear regression model error: ' + str(lrerror / 10.0)
        print 'polynomial mode error: ' + str(polyerror / 10.0)
        print 'logistic mode error: ' + str(logierror / 10.0)
        print '\n'


print "aggregate file:"
time_range = [key for key, value in time_dict_aggregate.iteritems()]
del time_range[len(time_range) - 1]

feature = [value for key, value in time_dict_aggregate.iteritems()]
del feature[len(feature) - 1]

label = [value[0] for key, value in time_dict_aggregate.iteritems()]
del label[0]

# first is the first begining to 02/01/8:00
print "the first begining to 02/01/8:00"
superbowl_start = time_range.index(752)
label_before = np.array(label[0:superbowl_start])
feature_before = np.array(feature[0:superbowl_start])

lrerror = 0
polyerror = 0
logierror = 0

kf = KFold(n_splits=10, shuffle=True)
for train_index, test_index in kf.split(feature_before):
    features_train, labels_train = feature_before[train_index], label_before[train_index]
    features_test, labels_test = feature_before[test_index], label_before[test_index]
    # Linear Regression
    lr = linear_model.LinearRegression()
    lr.fit(features_train, labels_train)
    test_predict = lr.predict(features_test)
    lrerror += math.sqrt(mean_squared_error(test_predict, labels_test))

    # Polynomial Regression
    poly = PolynomialFeatures(2)
    polymodel = linear_model.LinearRegression()
    polymodel.fit(poly.fit_transform(features_train), labels_train)
    test_predict = polymodel.predict(poly.fit_transform(features_test))
    polyerror += math.sqrt(mean_squared_error(test_predict, labels_test))

    # Logistic Regression
    logimodel = linear_model.LogisticRegression()
    logimodel.fit(features_train, labels_train)
    test_predict = logimodel.predict(features_test)
    logierror += math.sqrt(abs(mean_squared_error(test_predict, labels_test)))
print 'linear regression model error: ' + str(lrerror / 10.0)
print 'polynomial mode error: ' + str(polyerror / 10.0)
print 'logistic mode error: ' + str(logierror / 10.0)

# 02/01/8:00 to 8:00 PM
print "02/01/8:00 to 8:00 PM"
superbowl_start = time_range.index(752)
superbowl_end = time_range.index(764)
label_before = np.array(label[superbowl_start:superbowl_end])
feature_before = np.array(feature[superbowl_start:superbowl_end])

lrerror = 0
polyerror = 0
logierror = 0

kf = KFold(n_splits=10, shuffle=True)
for train_index, test_index in kf.split(feature_before):
    features_train, labels_train = feature_before[train_index], label_before[train_index]
    features_test, labels_test = feature_before[test_index], label_before[test_index]
    # Linear Regression
    lr = linear_model.LinearRegression()
    lr.fit(features_train, labels_train)
    test_predict = lr.predict(features_test)
    lrerror += math.sqrt(mean_squared_error(test_predict, labels_test))

    # Polynomial Regression
    poly = PolynomialFeatures(2)
    polymodel = linear_model.LinearRegression()
    polymodel.fit(poly.fit_transform(features_train), labels_train)
    test_predict = polymodel.predict(poly.fit_transform(features_test))
    polyerror += math.sqrt(mean_squared_error(test_predict, labels_test))

    # Logistic Regression
    logimodel = linear_model.LogisticRegression()
    logimodel.fit(features_train, labels_train)
    test_predict = logimodel.predict(features_test)
    logierror += math.sqrt(abs(mean_squared_error(test_predict, labels_test)))
print 'linear regression model error: ' + str(lrerror / 10.0)
print 'polynomial mode error: ' + str(polyerror / 10.0)
print 'logistic mode error: ' + str(logierror / 10.0)

# 02/01/8:00 PM to end
print "02/01/8:00 PM to end"
superbowl_end = time_range.index(765)
label_before = np.array(label[superbowl_end:])
feature_before = np.array(feature[superbowl_end:])

lrerror = 0
polyerror = 0
logierror = 0

kf = KFold(n_splits=10, shuffle=True)
for train_index, test_index in kf.split(feature_before):
    features_train, labels_train = feature_before[train_index], label_before[train_index]
    features_test, labels_test = feature_before[test_index], label_before[test_index]
    # Linear Regression
    lr = linear_model.LinearRegression()
    lr.fit(features_train, labels_train)
    test_predict = lr.predict(features_test)
    lrerror += math.sqrt(mean_squared_error(test_predict, labels_test))

    # Polynomial Regression
    poly = PolynomialFeatures(2)
    polymodel = linear_model.LinearRegression()
    polymodel.fit(poly.fit_transform(features_train), labels_train)
    test_predict = polymodel.predict(poly.fit_transform(features_test))
    polyerror += math.sqrt(mean_squared_error(test_predict, labels_test))

    # Logistic Regression
    logimodel = linear_model.LogisticRegression()
    logimodel.fit(features_train, labels_train)
    test_predict = logimodel.predict(features_test)
    logierror += math.sqrt(abs(mean_squared_error(test_predict, labels_test)))
print 'linear regression model error: ' + str(lrerror / 10.0)
print 'polynomial mode error: ' + str(polyerror / 10.0)
print 'logistic mode error: ' + str(logierror / 10.0)
print '\n'
