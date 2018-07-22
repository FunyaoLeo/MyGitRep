import numpy as np
from sklearn.model_selection import KFold
from sklearn import linear_model
from sklearn import metrics

movie_genre = {}
genres = []
with open("movie_genre.txt", "r") as genre_file:
        for line in genre_file:
            line = line[:-1]
            line_break = line.split("\t\t")
            movie_genre[line_break[0]] = line_break[1]
            if line_break[1] not in genres:
                genres.append(line_break[1])
genre_file.close()

rating_dict = {}
with open("movie_rating.txt", "r") as rating_file:
    for line in rating_file:
        line = line[:-1]
        line_break = line.split("\t\t")
        rating_dict[line_break[0]] = float(line_break[1])
rating_file.close()

rating_dict_keys = rating_dict.keys()
kf = KFold(n_splits=2, shuffle=True)
for train_indexs, test_indexs in kf.split(rating_dict_keys):
    # TRAINING START. ALL THE VARIABLES ARE TRAINING
    train_rating_dict = {}
    for train_index in train_indexs:
        train_rating_dict[rating_dict_keys[train_index]] = rating_dict[rating_dict_keys[train_index]]

    director_rating = {}
    movie_director_rating = {}
    with open("director.txt", "r") as director_file:
        for line in director_file:
            line = line[:-1]
            line_break = line.split("\t\t")
            num_movies = len(line_break)
            director = line_break[0]
            total_rating = 0.0
            real_movie_num = 0
            for num_movie in range(1, num_movies):
                if line_break[num_movie] in train_rating_dict:
                    real_movie_num = real_movie_num + 1
                    total_rating = total_rating + train_rating_dict[line_break[num_movie]]
            if real_movie_num != 0:
                total_rating = total_rating * 1.0 / real_movie_num
                director_rating[director] = total_rating
    director_file.close()

    with open("director.txt", "r") as director_file:
        with open("movie_director_rating.txt", "w") as director_rating_file:
            for line in director_file:
                line = line[:-1]
                line_break = line.split("\t\t")
                num_movies = len(line_break)
                director = line_break[0]
                if director in director_rating:
                    for num_movie in range(1, num_movies):
                        if line_break[num_movie] in train_rating_dict:
                            director_rating_file.write(
                                line_break[num_movie] + "\t\t" + str(director_rating[director]) + "\n")
                            movie_director_rating[line_break[num_movie]] = director_rating[director]
        director_rating_file.close()
    director_file.close()

    actor_rating = {}
    movie_actor = {}
    movie_actor_rating = {}
    with open("merge.txt", "r") as actor_file:
        for line in actor_file:
            line = line[:-1]
            line_break = line.split("\t\t")
            num_movies = len(line_break)
            actor = line_break[0]
            total_rating = 0.0
            real_movie_num = 0
            for num_movie in range(1, num_movies):
                if line_break[num_movie] in train_rating_dict:
                    if line_break[num_movie] in movie_actor:
                        movie_actor[line_break[num_movie]].append(actor)
                    else:
                        movie_actor[line_break[num_movie]] = [actor]

                    real_movie_num = real_movie_num + 1
                    total_rating = total_rating + train_rating_dict[line_break[num_movie]]
            if real_movie_num != 0:
                total_rating = total_rating * 1.0 / real_movie_num
                actor_rating[actor] = total_rating
    actor_file.close()

    with open("movie_merge_rating.txt", "w") as actor_rating_file:
        for key in movie_actor:
            actor_num = 0
            rating = 0
            for actor in movie_actor[key]:
                if actor in actor_rating:
                    actor_num = actor_num + 1
                    rating = rating + actor_rating[actor]
            if actor_num != 0 and key != "":
                movie_actor_rating[key] = rating * 1.0 / actor_num
                actor_rating_file.write(key + "\t\t" + str(rating * 1.0 / actor_num) + "\n")
    actor_rating_file.close()

    train_labels = []
    train_features = []
    for key in train_rating_dict:
        if key in movie_actor and key in movie_director_rating and key in movie_actor_rating and key in movie_genre:
            genre_feature = np.zeros(len(genres)).tolist()
            genre_feature[genres.index(movie_genre[key])] = 1
            actor_sort = []
            feature = []

            for actor in movie_actor[key]:
                if actor in actor_rating:
                    actor_sort.append(actor_rating[actor])
            if len(actor_sort) < 5:
                continue
            actor_sort.sort(reverse=True)
            feature = actor_sort[0:5]

            feature.append(movie_director_rating[key])
            feature.append(movie_actor_rating[key])
            feature.append(np.var(actor_sort))
            feature = feature + genre_feature
            train_labels.append(train_rating_dict[key])
            train_features.append(feature)
    train_labels = np.array(train_labels)
    train_features = np.array(train_features)



    # TESTING START. ALL THE VARIABLES ARE TESTING
    test_rating_dict = {}
    for test_index in test_indexs:
        test_rating_dict[rating_dict_keys[test_index]] = rating_dict[rating_dict_keys[test_index]]

    director_rating = {}
    movie_director_rating = {}
    with open("director.txt", "r") as director_file:
        for line in director_file:
            line = line[:-1]
            line_break = line.split("\t\t")
            num_movies = len(line_break)
            director = line_break[0]
            total_rating = 0.0
            real_movie_num = 0
            for num_movie in range(1, num_movies):
                if line_break[num_movie] in test_rating_dict:
                    real_movie_num = real_movie_num + 1
                    total_rating = total_rating + test_rating_dict[line_break[num_movie]]
            if real_movie_num != 0:
                total_rating = total_rating * 1.0 / real_movie_num
                director_rating[director] = total_rating
    director_file.close()

    with open("director.txt", "r") as director_file:
        with open("movie_director_rating.txt", "w") as director_rating_file:
            for line in director_file:
                line = line[:-1]
                line_break = line.split("\t\t")
                num_movies = len(line_break)
                director = line_break[0]
                if director in director_rating:
                    for num_movie in range(1, num_movies):
                        if line_break[num_movie] in test_rating_dict:
                            director_rating_file.write(
                                line_break[num_movie] + "\t\t" + str(director_rating[director]) + "\n")
                            movie_director_rating[line_break[num_movie]] = director_rating[director]
        director_rating_file.close()
    director_file.close()

    actor_rating = {}
    movie_actor = {}
    movie_actor_rating = {}
    with open("merge.txt", "r") as actor_file:
        for line in actor_file:
            line = line[:-1]
            line_break = line.split("\t\t")
            num_movies = len(line_break)
            actor = line_break[0]
            total_rating = 0.0
            real_movie_num = 0
            for num_movie in range(1, num_movies):
                if line_break[num_movie] in test_rating_dict:
                    if line_break[num_movie] in movie_actor:
                        movie_actor[line_break[num_movie]].append(actor)
                    else:
                        movie_actor[line_break[num_movie]] = [actor]

                    real_movie_num = real_movie_num + 1
                    total_rating = total_rating + test_rating_dict[line_break[num_movie]]
            if real_movie_num != 0:
                total_rating = total_rating * 1.0 / real_movie_num
                actor_rating[actor] = total_rating
    actor_file.close()

    with open("movie_merge_rating.txt", "w") as actor_rating_file:
        for key in movie_actor:
            if key in test_rating_dict:
                actor_num = 0
                rating = 0
                for actor in movie_actor[key]:
                    if actor in actor_rating:
                        actor_num = actor_num + 1
                        rating = rating + actor_rating[actor]
                if actor_num != 0 and key != "":
                    movie_actor_rating[key] = rating * 1.0 / actor_num
                    actor_rating_file.write(key + "\t\t" + str(rating * 1.0 / actor_num) + "\n")
    actor_rating_file.close()

    test_labels = []
    test_features = []
    for key in test_rating_dict:
        if key in movie_actor and key in movie_director_rating and key in movie_actor_rating and key in movie_genre:
            genre_feature = np.zeros(len(genres)).tolist()
            genre_feature[genres.index(movie_genre[key])] = 1
            actor_sort = []
            feature = []

            for actor in movie_actor[key]:
                if actor in actor_rating:
                    actor_sort.append(actor_rating[actor])
            if len(actor_sort) < 5:
                continue
            actor_sort.sort(reverse=True)
            feature = actor_sort[0:5]

            feature.append(movie_director_rating[key])
            feature.append(movie_actor_rating[key])
            feature.append(np.var(actor_sort))
            feature = feature + genre_feature
            test_labels.append(test_rating_dict[key])
            test_features.append(feature)
    test_labels = np.array(test_labels)
    test_features = np.array(test_features)

    lr = linear_model.LinearRegression()
    lr.fit(train_features, train_labels)
    labels_train_predict = lr.predict(train_features)
    print "training error"
    print(np.sqrt(metrics.mean_squared_error(train_labels, labels_train_predict)))
    labels_test_predict = lr.predict(test_features)
    print "testing error"
    print(np.sqrt(metrics.mean_squared_error(test_labels, labels_test_predict)))
