import re
import codecs

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


f_w = codecs.open('./director.txt', 'w', encoding='latin1')
actor_movie = {}
actress_movie = {}
movie_performer = {}
with codecs.open('./director_movies.txt', 'r', encoding='latin1') as actor_file:
    for line in actor_file:
        temp = line.split('\t\t')
        if len(temp) >= 6:
            # sublist = []
            f_w.write(temp[0])
            for i in range(1,len(temp)):
                temp_1 = re.sub("[\(|\{][^0-9XIV\?\s]*[\(|\{]", "", temp[i])
                temp_1 = re.sub("\([^0-9\?{4,}][^\)]+\)", "", temp_1)
                temp_1 = temp_1.rstrip()
                f_w.write('\t\t' + temp_1)
            f_w.write('\n')
            #     sublist.append(temp_1)
            #     if temp_1 not in movie_performer.keys():
            #         movie_performer[temp_1] = [temp[0]]
            #     else:
            #         movie_performer[temp_1].append(temp[0])
            # actor_movie[temp[0]] = sublist
actor_file.close()
"""
with codecs.open('./actress_movies.txt', 'r', encoding='latin1') as actress_file:
    for line in actress_file:
        temp = line.split('\t\t')
        if len(temp) >= 11:
            # sublist = []
            f_w.write(temp[0])
            for i in range(1, len(temp)):
                temp_1 = re.sub("[\(|\{][^0-9XIV\?\s]*[\(|\{]", "", temp[i]) #^a-zA-Z0-9\?\s
                temp_1 = re.sub("\([^0-9\?{4,}][^\)]+\)", "", temp_1)
                temp_1 = temp_1.rstrip()
                f_w.write('\t\t' + temp_1)
            f_w.write('\n')
            #     sublist.append(temp_1)
            #     if temp_1 not in movie_performer.keys():
            #         movie_performer[temp_1] = [temp[0]]
            #     else:
            #         movie_performer[temp_1].append(temp[0])
            # actor_movie[temp[0]] = sublist
actress_file.close()

f_w.close()

# performer_movie = merge_two_dicts(actor_movie, actress_movie)
# print(len(movie_performer))
# print(len(performer_movie))
#
# for key in movie_performer.keys():
#     if len(movie_performer[key]) < 5:
#         del movie_performer[key]

# print(movie_performer[:100])
# print(performer_movie[:100])
"""
with codecs.open('./director.txt', 'r', encoding='latin1') as actor_file:
    i=1
    for line in actor_file:
        i=i+1
        print line
        if i>10:
            break
actor_file.close()

with codecs.open('./director_movies.txt', 'r', encoding='latin1') as actor_file:
    i=1
    for line in actor_file:
        i=i+1
        print line
        if i>10:
            break
actor_file.close()
