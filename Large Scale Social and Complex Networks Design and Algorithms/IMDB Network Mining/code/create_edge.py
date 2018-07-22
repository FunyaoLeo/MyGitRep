import codecs
import itertools
import time
import copy


movie_list = set()
num_performer = 0
total_movie = 0
with codecs.open('./data/merge.txt', 'r', encoding='latin1') as f:
    for line in f:
        temp = line.rstrip().split('\t\t')
        total_movie += len(temp) - 1
        for i in range(1, len(temp)):
            movie_list.update([temp[i]])
        num_performer += 1
f.close()

print(total_movie)
print(len(movie_list))
print(num_performer)


#create edge list
start_time = time.time()
movie_list = list(movie_list)
movie_performer = {}
count = 0
with codecs.open('./data/merge.txt', 'r', encoding='latin1') as f:
    last = time.time()
    for line in f:
        temp = line.rstrip().split('\t\t')
        count += 1
        for i in range(1, len(temp)):
            if temp[i] not in movie_performer:
                movie_performer[temp[i]] = [temp[0]]
            else:
                movie_performer[temp[i]].append(temp[0])
        if count % 2000 == 0:
            print('Processed %s performers at %s' % (str(count), str(time.time() - last)))
            last = time.time()
f.close()

print('Total length: %s' % str(time.time() - start_time))
print('Length of unique movies: %d' % len(movie_list))
print('Length of dictionary: %d' % len(movie_performer))


# Filter movie which have performers less than 5
count_1 = 0
r = 0
num = len(movie_performer)
key_list = movie_performer.keys()
mp_temp = copy.deepcopy(movie_performer)
for i in range(num):
    if len(mp_temp[key_list[i]]) < 5:
        del movie_performer[key_list[i]]
        continue
    count_1 += 1

print("Following numbers should be consistent:")
print(count_1)
print(len(movie_performer))


# Method 1
values = movie_performer.values()
keys = movie_performer.keys()

# Compute the similarity among movies by comparing lists of performers
def compute_similarity_1(a, b):
    p = set(values[a])
    q = set(values[b])
    return len(p & q)/float(len(p | q))


f_w = codecs.open('./data/edge_list_v2.txt', 'w', encoding='latin1')
s = time.time()
count = 0
total_movie = len(movie_performer)
for i in range(total_movie):
    count += 1
    for j in range(i+1, total_movie):
        weight = compute_similarity_1(i, j)
        if weight > 0:
            edge_1 = keys[i]
            edge_2 = keys[j]
            f_w.write(edge_1 + '\t\t' + edge_2 + '\t\t' + str(weight) + '\n')
    if count % 1000 == 0:
        print('Processed %s / %s movies in %s sec' % (str(count), str(total_movie), str(time.time() - s)))
        s = time.time()
f_w.close()

# Method 2
# def compute_similarity_1(a,b):
#     p = set(movie_performer[a])
#     q = set(movie_performer[b])
#     return len(p & q)/float(len(p | q))
#
#
# f_w = codecs.open('./data/edge_list_v3.txt', 'w', encoding='latin1')
# s = time.time()
# count = 0
# i = 0
# total_movie = len(movie_performer)
# keys = movie_performer.keys()
# for key_1 in keys:
#     j = 0
#     count += 1
#     for key_2 in keys:
#         j += 1
#         if i < j:
#             weight = compute_similarity_1(key_1, key_2)
#             if weight > 0:
#                 edge_1 = key_1
#                 edge_2 = key_2
#                 f_w.write(edge_1 + '\t\t' + edge_2 + '\t\t' + str(weight) + '\n')
#     if count % 1000 == 0:
#         print('Processed %s / %s movies at %s' % (str(count), str(total_movie), str(time.time() - s)))
#         s = time.time()
#     i += 1
# f_w.close()
