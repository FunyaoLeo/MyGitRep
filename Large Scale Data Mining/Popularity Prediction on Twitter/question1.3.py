from statsmodels.regression.linear_model import OLS
from statsmodels.api import add_constant
import json,os
import math
import datetime
import pytz
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np

def min_three(pvalue_list):
    p_index=[]
    for i in range(3):
        min_value=min(pvalue_list)
        a=pvalue_list.index(min_value)
        pvalue_list[a]=1
        p_index.append(a)
    return p_index
data_path="./tweet_data"
min_data = 1000000000
max_data = 0
# [number of tweets,   sum of "favorite_count" , max number of favorite_count ,  "ranking_score" ,"sum friends_count"]
feature_list=["number of tweets", "sum of favourites_count" , "max number of favourite_count" , "ranking_score", "sum of friends_count"]
for file_name in os.listdir(data_path):
    number_of_tweets = 0
    number_of_retweets = 0
    number_of_followers = 0
    time_dict={}
    feature=[]
    label=[]
    max_time=0
    min_time=100000000
    if file_name.endswith(".txt"):
        with open(os.path.join(data_path,file_name)) as text:
            print file_name
            for i,line in enumerate(text):
                json_object=json.loads(line)
                """if i==1:
                    print json_object['tweet']['user']['favourites_count']
                    print json_object['metrics']['ranking_score']
                    print json_object['tweet']['user']['friends_count']"""
                number_of_tweets += 1
                time = json_object['citation_date']
                pst_tz=pytz.timezone('US/Pacific')
                time=datetime.datetime.fromtimestamp(time, pst_tz)
                tmp=(time.month-1)*31*24+(time.day-1)*24+time.hour
                if max_time<tmp:
                    max_time=tmp
                if min_time>tmp:
                    min_time=tmp
                if tmp not in time_dict:
                    time_dict.setdefault(tmp,[0,0,0,0,0])
                if tmp in time_dict:
                    time_dict[tmp][0]+=1
                    time_dict[tmp][1]+=json_object['tweet']['user']['favourites_count']
                    time_dict[tmp][3]+=json_object['metrics']['ranking_score']
                    time_dict[tmp][4]+=json_object['tweet']['user']['friends_count']
                    if json_object['tweet']['user']['favourites_count']>time_dict[tmp][2]:
                        time_dict[tmp][2]=json_object['tweet']['user']['favourites_count']
            for i in range(min_time, max_time + 1):
                if i not in time_dict.keys():
                    time_dict.setdefault(i, [0,0,0,0,0])
            #print time_dict
            feature=[value for key, value in time_dict.iteritems()]
            del feature[len(feature)-1]
            label=[value[0] for key ,value in time_dict.iteritems()]
            del label[0]
            x_train,x_test,y_train,y_test=train_test_split(feature,label,test_size=0.2,random_state=42)
            lr=linear_model.LinearRegression()
            lr.fit(x_train,y_train)
            test_predict=lr.predict(x_test)
            #print "test_predict"
            #print test_predict
            print "rmse = % f" %( math.sqrt(mean_squared_error(test_predict,y_test)))
            model=OLS(label,feature)
            results=model.fit()
            print "p_values: "
            print results.pvalues
            feature_select=min_three(results.pvalues.tolist())
            print "most three important features:"
            print " %s    %s     %s" %(feature_list[feature_select[0]],feature_list[feature_select[1]],feature_list[feature_select[2]])
            print "plot scatters:"
            x_test=np.array(x_test)
            for i in range(3):
                plt.scatter(x_test[:,feature_select[i]],test_predict,label=feature_list[feature_select[i]])
                plt.legend()
                plt.show()

            #print "t_test :"
            #print results.t_test(results.params)
            #print "summary"
            #print results.summary()
            print "======================"