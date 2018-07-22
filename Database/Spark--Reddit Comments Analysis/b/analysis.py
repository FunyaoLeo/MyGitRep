import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from sklearn.metrics import roc_curve, auc  

from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon


"""
PLOT 1: SENTIMENT OVER TIME (TIME SERIES PLOT)
"""

#read data
ts1 = pd.read_csv("task10_2_pos.csv")
ts2 = pd.read_csv("task10_2_neg.csv")
del ts1['Unnamed: 0']
del ts1['count_day']
del ts2['Unnamed: 0']
del ts2['count_day']
ts = pd.merge(ts1,ts2,on='day')
ts.columns = ['day','positive','negative']
print ts.columns
# Remove erroneous row.
ts = ts[ts['day'] != '2018-12-31']

plt.figure(figsize=(12,5))
ts.date = pd.to_datetime(ts['day'], format='%Y-%m-%d')
ts.set_index(['day'],inplace=True)

ax = ts.plot(title="President Trump Sentiment on /r/politics Over Time",
        color=['green', 'red'],
       ylim=(0, 1.05))
ax.plot()
plt.savefig("part1.png")
plt.close()


"""
PLOT 2: SENTIMENT BY STATE (POSITIVE AND NEGATIVE SEPARATELY)
# This example only shows positive, I will leave negative to you.
"""

#prepare state data
state_data_pos = pd.read_csv("task10_3_pos.csv")
state_data_neg = pd.read_csv("task10_3_neg.csv")
del state_data_pos['Unnamed: 0']
del state_data_neg['Unnamed: 0']
del state_data_pos['count_state']
del state_data_neg['count_state']
state_data = pd.merge(state_data_pos, state_data_neg, on='state')

state_data.columns = ['state', 'Positive', 'Negative']


# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
        projection='lcc', lat_1=33, lat_2=45, lon_0=-95)
shp_info = m.readshapefile('st99_d00','states',drawbounds=True)  # No extension specified in path here.
pos_data = dict(zip(state_data.state, state_data.Positive))
neg_data = dict(zip(state_data.state, state_data.Negative))

# choose a color for each state based on sentiment.
pos_colors = {}
statenames = []
pos_cmap = plt.cm.Greens # use 'hot' colormap

vmin = 0; vmax = 1 # set range.
for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia', 'Puerto Rico']:
        pos = pos_data[statename]
        pos_colors[statename] = pos_cmap(1. - np.sqrt(( pos - vmin )/( vmax - vmin)))[:3]
    statenames.append(statename)
# cycle through state names, color each one.

# POSITIVE MAP
ax = plt.gca() # get current axes instance
for nshape, seg in enumerate(m.states):
    # skip Puerto Rico and DC
    if statenames[nshape] not in ['District of Columbia', 'Puerto Rico']:
        color = rgb2hex(pos_colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)
plt.title('Positive Trump Sentiment Across the US')
plt.savefig("mycoolmap.png")
plt.close()


"""
PLOT 5A: SENTIMENT BY STORY SCORE
"""
# What is the purpose of this? It helps us determine if the story score
# should be a feature in the model. Remember that /r/politics is pretty
# biased.

# Assumes a CSV file called submission_score.csv with the following coluns
# submission_score, Positive, Negative

story_pos = pd.read_csv("task10_42_pos.csv")
story_neg = pd.read_csv("task10_42_neg.csv")
del story_pos['Unnamed: 0']
del story_neg['Unnamed: 0']
story = pd.merge(story_pos, story_neg, on=['story_score'])
story.columns = ['Story score','Positive','Negative']

plt.figure(figsize=(12,5))
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.scatter(story['Story score'], story['Positive'], s=10, c='b', marker="s", label='Positive')
ax1.scatter(story['Story score'], story['Negative'], s=10, c='r', marker="o", label='Negative')
plt.legend(loc='lower right');

plt.xlabel('President Trump Sentiment by Submission Score')
plt.ylabel("Percent Sentiment")
plt.savefig("plot5a.png")
plt.close()


"""
PLOT 5B: SENTIMENT BY COMMENT SCORE
"""
# What is the purpose of this? It helps us determine if the comment score
# should be a feature in the model. Remember that /r/politics is pretty
# biased.

# Assumes a CSV file called comment_score.csv with the following columns
# comment_score, Positive, Negative

story_pos = pd.read_csv("task10_41_pos.csv")
story_neg = pd.read_csv("task10_41_neg.csv")
del story_pos['Unnamed: 0']
del story_neg['Unnamed: 0']
story = pd.merge(story_pos, story_neg, on=['comment_score'])

story.columns = ['comment_score','Positive','Negative']
plt.figure(figsize=(12,5))
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.scatter(story['comment_score'], story['Positive'], s=10, c='b', marker="s", label='Positive')
ax1.scatter(story['comment_score'], story['Negative'], s=10, c='r', marker="o", label='Negative')
plt.legend(loc='lower right');

plt.xlabel('President Trump Sentiment by Comment Score')
plt.ylabel("Percent Sentiment")
plt.savefig("plot5b.png")
plt.close()


# ROC Plot

pro = pd.read_csv("pos_probability.csv")
pro_array = []
label_array = []
[row, col] = pro.shape
pro_value = pro.values
for i in range(row):
    tmp = []
    label = pro_value[i][1]
    df = pro_value[i][2].split(',')
    pos_str = df[1].strip(']')
    possibility = float(pos_str)
    pro_array.append(possibility)
    label_array.append(label)

pfpr, ptpr, pthresholds = roc_curve(label_array, pro_array)
proc_auc = auc(pfpr, ptpr)

neg = pd.read_csv("neg_probability.csv")
neg_array = []
label_array = []
[row, col] = neg.shape
neg_value = neg.values
for i in range(row):
    tmp = []
    label = neg_value[i][1]
    df = neg_value[i][2].split(',')
    neg_str = df[0].strip('[')
    possibility = float(neg_str)
    neg_array.append(possibility)
    label_array.append(label)

nfpr, ntpr, nthresholds = roc_curve(label_array, neg_array)
neg_auc = auc(nfpr, ntpr)
plt.figure(figsize=(12,9))
plt.title('Receiver operating characteristic')
plt.plot(pfpr, ptpr, lw=1, label='Trump Positive Sentiment: ROC (area = %0.2f)' % (proc_auc))
plt.plot(nfpr, ntpr, lw=1, label='Trump Negative Sentiment: ROC (area = %0.2f)' % (neg_auc))
plt.legend(loc = 'best')
plt.savefig("plot6.png")
plt.close()
print proc_auc
print neg_auc
