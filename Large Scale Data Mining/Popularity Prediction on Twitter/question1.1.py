import json,os
import datetime
import pytz
import matplotlib.pyplot as plt
data_path="./tweet_data"
min_data = 1000000000
max_data = 0
for file_name in os.listdir(data_path):
    number_of_tweets = 0
    number_of_retweets = 0
    number_of_followers = 0
    time_dict={}
    max_time=0
    min_time=100000000
    #mat=0
    #mit=0
    if file_name.endswith(".txt"):
        with open(os.path.join(data_path,file_name)) as text:
            print file_name
            for i,line in enumerate(text):
                json_object=json.loads(line)
                number_of_tweets += 1
                number_of_followers += json_object['author']['followers']
                number_of_retweets += json_object['metrics']['citations']['total']
                time = json_object['citation_date']
                pst_tz=pytz.timezone('US/Pacific')
                time=datetime.datetime.fromtimestamp(time, pst_tz)
                tmp=(time.month-1)*31*24+(time.day-1)*24+time.hour
                if max_time<tmp:
                    max_time=tmp
                    #mat=time
                if min_time>tmp:
                    min_time=tmp
                   # mit=time
                if tmp not in time_dict:
                    time_dict.setdefault(tmp,1)
                if tmp in time_dict:
                    time_dict[tmp]+=1

            for i in range(min_time, max_time + 1):
                if i not in time_dict.keys():
                    time_dict.setdefault(i, 0)
            print 'Average number of tweets per hour: %f' % (number_of_tweets/float(max_time-min_time+1))
            print 'Average number of followers of users posting the tweets: %f' % (number_of_followers/float(number_of_tweets))
            print 'Average number of retweets: %f' % (number_of_retweets/float(number_of_tweets))
    if file_name=="tweets_#nfl.txt" or file_name=="tweets_#superbowl.txt":
        plt.plot([i for i in range(len(time_dict))],[value for key, value in time_dict.items()],label=file_name.rstrip('.txt'))
        plt.legend()
        plt.show()
