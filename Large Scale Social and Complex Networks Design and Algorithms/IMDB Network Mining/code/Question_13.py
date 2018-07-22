import codecs
import time
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np


def rmse(y_actual, y_predicted):
	return sqrt(mean_squared_error(y_actual, y_predicted))


def mean(l):
	return sum(l) / float(len(l))


movie_rate = {}
with codecs.open('./data/movie_rating.txt', 'r', encoding='latin1') as f:
	for line in f:
		sent = line.rstrip().split('\t\t')
		# print(sent[0])
		# print(sent[1])
		movie_rate[sent[0]] = float(sent[1])

# Read merging list
start_time = time.time()
movie_performer = {}
performer_movie = {}
count = 0
with codecs.open('./data/merge_1.txt', 'r', encoding='latin1') as f:
	last = time.time()
	for line in f:
		temp = line.rstrip().split('\t\t')
		performer_movie[temp[0]] = temp[1:]
		count += 1
		for i in range(1, len(temp)):
			if temp[i] not in movie_performer:
				movie_performer[temp[i]] = [temp[0]]
			else:
				movie_performer[temp[i]].append(temp[0])
		if count % 10000 == 0:
			print('Processed %s performers at %s' % (str(count), str(time.time() - last)))
			last = time.time()
print('Total time: %s' % str(time.time() - start_time))
print('Length of dictionary: %d' % len(movie_performer))
print('='*50 + '\n' + 'Movie2performer and Performer2movie are done.' + '\n' + '='*50)

# # Create the rate for each performer
# start_time = time.time()
# performer_rate = {}
# for key in performer_movie.keys()[:10]:
# 	rate_list = []
# 	ml = performer_movie[key]
# 	for movie in ml:
# 		if movie in movie_rate.keys():
# 			rate_list.append(movie_rate[movie])
# 	if len(rate_list) == 0:
# 		performer_rate[key] = 0
# 		continue
# 	E_rate = mean(rate_list)
# 	M_rate = max(rate_list)
# 	performer_rate[key] = 0.2 * M_rate + 0.8 * E_rate
# print(performer_rate.items())
# print('Total time for performer2rate: %s' % str(time.time() - start_time))
# print('='*10 + '\n' + 'Performer2rate is done.' + '\n' + '='*10)
#
# # Build Bipartite graph
# movie_list = ["Batman v Superman: Dawn of Justice (2016)", "Mission: Impossible - Rogue Nation (2015)", "Minions (2015)"]
# for movie in movie_list:
# 	rate_list = []
# 	for per in movie_performer[movie]:
# 		if per in performer_rate.keys():
# 			rate_list.append(performer_rate[per])
# 	print('Rate of %s is predicted as %f' % (movie, mean(rate_list)))

# Create test set
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(movie_rate)))
test = np.asarray(movie_rate.keys())[shuffle_indices]
test = list(test[:200])


def per2score(perf):
	mt = performer_movie[perf]
	rt = []
	for m in mt:
		if m in movie_rate.keys():
			rt.append(movie_rate[m])
	if len(rt) == 0:
		return 0
	E = mean(rt)
	# print('E: %f' % E)
	M = max(rt)
	# print('M: %f' % M)
	return 0.2 * M + 0.8 * E


# Build Bipartite graph
# y_a = []
# y_p = []
# for movie in test:
# 	rate_list = []
# 	if movie in movie_performer.keys():
# 		for per in movie_performer[movie]:
# 			rate_list.append(per2score(per))
# 		if mean(rate_list) != 0:
# 			y_p.append(mean(rate_list))
# 			y_a.append(movie_rate[movie])
# error = rmse(y_a, y_p)
# print('RMSE of test set: %f' % error)



movie_list = ["Batman v Superman: Dawn of Justice (2016)", "Mission: Impossible - Rogue Nation (2015)", "Minions (2015)"]
y_a = [6.6, 7.4, 6.4]
y_p = []
for movie in movie_list:
	rate_list = []
	for per in movie_performer[movie]:
		rate_list.append(per2score(per))
	y_p.append(mean(rate_list))
	print('Rate of %s is predicted as %f' % (movie, mean(rate_list)))
error = rmse(y_a, y_p)
print('RMSE of test set: %f' % error)


