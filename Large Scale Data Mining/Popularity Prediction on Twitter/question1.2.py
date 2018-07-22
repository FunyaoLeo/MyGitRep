from statsmodels.regression.linear_model import OLS
from statsmodels.api import add_constant
import numpy as np
import json,os
import math
import datetime
import pytz
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
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
    if file_name.endswith(".txt"):
        with open(os.path.join(data_path,file_name)) as text:
            print file_name
            a=[]
            for i,line in enumerate(text):
                json_object=json.loads(line)
                number_of_tweets += 1
                number_of_followers += json_object['author']['followers']
                number_of_retweets += json_object['metrics']['citations']['total']
                time = json_object['citation_date']
                pst_tz=pytz.timezone('US/Pacific')
                time=datetime.datetime.fromtimestamp(time, pst_tz)
                a.append(json_object['metrics']['citations']['total'])
                tmp=(time.month-1)*31*24+(time.day-1)*24+time.hour
                if max_time<tmp:
                    max_time=tmp
                if min_time>tmp:
                    min_time=tmp
                if tmp not in time_dict:
                    time_dict.setdefault(tmp,[0,0,0,0,0])
                    time_dict[tmp][4] = time.hour
                if tmp in time_dict:
                    time_dict[tmp][0]+=1
                    time_dict[tmp][1]+=json_object['metrics']['citations']['total']
                    time_dict[tmp][2]+=json_object['author']['followers']
                    if json_object['author']['followers']>time_dict[tmp][3]:
                        time_dict[tmp][3]=json_object['author']['followers']
            for i in range(min_time, max_time + 1):
                if i not in time_dict.keys():
                    time_dict.setdefault(i, [0,0,0,0,0])
            #plt.plot([i for i in range(len(a))],a)
            #plt.show()
            feature=[value for key, value in time_dict.iteritems()]
            del feature[len(feature)-1]
            label=[value[0] for key ,value in time_dict.iteritems()]
            del label[0]
            x_train,x_test,y_train,y_test=train_test_split(feature,label,test_size=0.2,random_state=42)
            lr=linear_model.LinearRegression()
            lr.fit(x_train,y_train)
            test_predict=lr.predict(x_test)
            feature=np.array(feature)
            print "rmse = % f" %( math.sqrt(mean_squared_error(test_predict,y_test)))
            model=OLS(label,feature)
            results=model.fit()
            print "p_values: "
            print results.pvalues
            print "t_test :"
            print results.t_test(results.params)
            print "summary"
            print results.summary()
            print "======================"
