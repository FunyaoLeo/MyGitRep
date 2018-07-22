import re
import codecs

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


f_w = codecs.open('./data/merge.txt', 'w', encoding='latin1')
actor_movie = {}
actress_movie = {}
movie_performer = {}
with codecs.open('./data/actor_movies.txt', 'r', encoding='latin1') as actor_file:
    for line in actor_file:
        temp = line.split('\t\t')
        if len(temp) >= 11:
            f_w.write(temp[0])
            for i in range(1,len(temp)):
                temp_1 = re.sub("[\(|\{][^0-9XIV\?\s]*[\(|\{]", "", temp[i])
                temp_1 = re.sub("\([^0-9\?{4,}][^\)]+\)", "", temp_1)
                temp_1 = temp_1.rstrip()
                f_w.write('\t\t' + temp_1)
            f_w.write('\n')
actor_file.close()

# Clean and create movie list
with codecs.open('./data/actress_movies.txt', 'r', encoding='latin1') as actress_file:
    for line in actress_file:
        temp = line.split('\t\t')
        if len(temp) >= 11:
            f_w.write(temp[0])
            for i in range(1, len(temp)):
                temp_1 = re.sub("[\(|\{][^0-9XIV\?\s]*[\(|\{]", "", temp[i])
                temp_1 = re.sub("\([^0-9\?{4,}][^\)]+\)", "", temp_1)
                temp_1 = temp_1.rstrip()
                f_w.write('\t\t' + temp_1)
            f_w.write('\n')
actress_file.close()

f_w.close()
