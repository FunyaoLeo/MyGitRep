"""
Author      : Fangyao Liu, Xuan Hu, Yanzhe Xu, Zhechen Xu
Description : ML utilties
"""
from util import *
from surprise import KNNWithMeans
from surprise import NMF
from surprise import SVD
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from surprise.model_selection import KFold
from surprise import accuracy
from sklearn import metrics
import matplotlib.pyplot as plt
import math
import numpy as np
import os


def main():

    ############################
    ##   Data Extraction   #####
    ############################
    # variables for question 1~6
    dataset = load_data_ratings('ratings.csv')
    userIds = dataset.userID
    movieIds = dataset.movieID
    ratings = dataset.ratings

    dataset_movie = load_data_movies('movies.csv')
    movie_dict = dict(zip(dataset_movie.movieID, dataset_movie.genres))

    num_of_user = max(userIds)
    print num_of_user

    movie_range = []
    for movieId in movieIds:
        if movieId not in movie_range:
            movie_range.append(movieId)
    num_of_movie = len(movie_range)
    print num_of_movie

    # variables for question 10 and rest
    file_path = os.path.expanduser('ratings.csv')
    reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0, 5), skip_lines=1)
    data = Dataset.load_from_file(file_path, reader=reader)
    print(data)



    # question 1: sparsity
    print ("Question 1 beigns")
    print("The sparsity of the " + str(1.0*len(ratings)/(num_of_user*num_of_movie)))

    # question 2:
    print ("Question 2 beigns")
    rating_range = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    plt.hist(ratings, bins=rating_range)
    plt.show()


    #question 3:
    print ("Question 3 beigns")
    id_ratings = zip(movieIds, ratings)
    id_ratings.sort()
    id_list = []
    rating_list =[ ]
    index = -1
    for i in range(len(id_ratings)):
        if id_ratings[i][0] not in id_list:
            id_list.append(id_ratings[i][0])
            rating_list.append(0)
            index += 1
        rating_list[index] += 1
    rating_id = zip(rating_list, id_list)
    rating_id.sort(reverse=True)
    rating_list, id_list = zip(*rating_id)
    plt.plot(rating_list)
    plt.show()

    #question 4:
    print ("Question 4 beigns")
    user=[]
    user_movie=[]

    #calculate the num
    for i in userIds:
        if i not in user:
            user.append(i)
            user_movie.append(userIds.count(i))

    result=zip(user_movie,user)
    result.sort(reverse=True)
    user_movie.sort(reverse=True)

    #plot
    plt.figure()
    plt.plot(user_movie)
    plt.xlabel("User")
    plt.ylabel("Num of Movies")
    plt.show()

    #question 5:

    #question 6:
    print ("Question 6 beigns")
    movie = []
    movie_rating = []
    tmp = []

    #calculate the variance
    movie.append(movieIds[0])
    for i in range(len(movieIds)):
        if movieIds[i] not in movie:
            movie.append(movieIds[i])
            var=np.var(tmp)
            tmp=[]
            movie_rating.append(var)

        tmp.append(ratings[i])

    var=np.var(tmp)
    movie_rating.append(var)

    #plot
    plt.figure()
    upper=math.floor(max(movie_rating)+1)
    bins=np.arange(0,upper,0.5)
    plt.xlim(0,upper)
    plt.hist(movie_rating[:],bins=bins,alpha=0.5)
    plt.xlabel("Variance")
    plt.ylabel("Num of Movie")
    plt.show()


    #problem 10: knn cross-validation
    print ("Question 10 beigns")
    rmse_range = []
    mae_range = []
    k_range = range(2, 101, 2)
    min_rmse = 1000.0
    min_mae = 1000.0
    k_min = 0
    for k in k_range:
        algo = KNNWithMeans(k=k, sim_options={'name': 'pearson'})
        dict = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=10)
        rmse = sum(dict['test_rmse'])/10.0
        mae = sum(dict['test_mae'])/10.0
        if(rmse<min_rmse and mae<min_mae):
            min_rmse = rmse
            min_mae = mae
            k_min = k
        rmse_range.append(rmse)
        mae_range.append(mae)
    plt.plot(k_range, rmse_range)
    plt.plot(k_range, mae_range)
    plt.show()


    kf = KFold(n_splits=10)
    k_range = range(2, 101,2)

    #Question12
    print ("Question 12 beigns")
    rmse=[]
    average_rmse=[]
    for k in k_range:
        algo = KNNWithMeans(k=k, sim_options={'name': 'pearson'})
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset=trim_dataset12(testset,2)
            predictions = algo.test(testset)
            rmse_temp=accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average=sum(rmse)/10.0
        average_rmse.append(rmse_average)
        rmse=[]
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)

    #Question13
    print ("Question 13 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = KNNWithMeans(k=k, sim_options={'name': 'pearson'})
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset = trim_dataset13(testset)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)


    #Question14
    print ("Question 14 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = KNNWithMeans(k=k, sim_options={'name': 'pearson'})
        for trainset, testset in kf.split(data):
            algo.fit(trainset)

            testset = trim_dataset14(testset)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)


    # question 15: plot roc curve and calculate the auc area
    print ("Question 15 beigns")
    pre_ratings=[]
    act_ratings=[]
    auc_area=[]
    binary_threadhold=[2.5,3,3.5,4]
    kf = KFold(n_splits=10)

    algo = KNNWithMeans(k=20, sim_options={'name': 'pearson'})
    trainset, testset = train_test_split(data,test_size=0.1)
    algo.fit(trainset)
    predictions = algo.test(testset)
    for i in range(len(predictions)):
        act_ratings.append(predictions[i][2])
        pre_ratings.append(predictions[i][3])

    for k in range(len(binary_threadhold)):
        binary_ratings=[]
        for i in range(len(act_ratings)):
            if(act_ratings[i]>=binary_threadhold[k]):
                binary_ratings.append(1)
            else:
                binary_ratings.append(0)
        fpr, tpr, threadhold = metrics.roc_curve(binary_ratings, pre_ratings, pos_label=1)
        auc_score=metrics.auc(fpr, tpr)
        auc_area.append(auc_score)
        print("Auc area is %f with threshold=%s" % (auc_score,str(binary_threadhold[k])))
        plt.figure()
        plt.plot(fpr, tpr)
        plt.title("ROC with threshold=%s" % str(binary_threadhold[k]))
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")



    # problem 17: NMF knn cross-validation
    print ("Question 17 beigns")
    NMF_rmse_range = []
    NMF_mae_range = []
    k_range = range(2, 51, 2)
    min_rmse = 1000.0
    min_mae = 1000.0
    k_min = 0
    for k in k_range:
        algo = NMF(n_factors=k)
        dict = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=10)
        rmse = sum(dict['test_rmse']) / 10.0
        mae = sum(dict['test_mae']) / 10.0
        if (rmse < min_rmse and mae < min_mae):
            min_rmse = rmse
            min_mae = mae
            k_min = k
        NMF_rmse_range.append(rmse)
        NMF_mae_range.append(mae)
    plt.plot(k_range, NMF_rmse_range)
    plt.plot(k_range, NMF_mae_range)
    plt.show()

    # question 18: find out the 'minimum k'
    print ("Question 18 beigns")
    print ("minimum k should be " + str(k_min))
    """

    """
    kf = KFold(n_splits=10)
    k_range = range(2, 51, 2)

    # Question19
    print ("Question 19 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = NMF(n_factors=k)
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset = trim_dataset12(testset, 2)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)

    # Question20
    print ("Question 20 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = NMF(n_factors=k)
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset = trim_dataset13(testset)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)

    # Question21
    print ("Question 21 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = NMF(n_factors=k)
        for trainset, testset in kf.split(data):
            algo.fit(trainset)

            testset = trim_dataset14(testset)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)


    # question 22: plot roc curve and calculate the auc area
    print ("Question 22 beigns")
    pre_ratings=[]
    act_ratings=[]
    auc_area=[]
    binary_threadhold=[2.5,3,3.5,4]

    trainset, testset = train_test_split(data,test_size=0.1)
    algo = NMF(n_factors=20)
    algo.fit(trainset)
    predictions = algo.test(testset)
    for i in range(len(predictions)):
        act_ratings.append(predictions[i][2])
        pre_ratings.append(predictions[i][3])

    for k in range(len(binary_threadhold)):
        binary_ratings=[]
        for i in range(len(act_ratings)):
            if(act_ratings[i]>=binary_threadhold[k]):
                binary_ratings.append(1)
            else:
                binary_ratings.append(0)
        fpr, tpr, threadhold = metrics.roc_curve(binary_ratings, pre_ratings, pos_label=1)
        auc_score=metrics.auc(fpr, tpr)
        auc_area.append(auc_score)
        print("Auc area is %f with threshold=%s" % (auc_score,str(binary_threadhold[k])))
        plt.figure()
        plt.plot(fpr, tpr)
        plt.title("ROC with threshold=%s" % str(binary_threadhold[k]))
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")



    # question 23: Interpretability of NNMF
    print ("Question 23 beigns")
    trainset = data.build_full_trainset()
    algo = NMF(n_factors=20, random_state=0)
    algo.fit(trainset)
    V_matrix = algo.qi.transpose()
    for column in range(20):
        rankings = np.argsort(-V_matrix[column])[0:10]

        print("column " + str(column))
        for ranking in rankings:
            raw_id = long(trainset.to_raw_iid(ranking))
            print(str(raw_id) + " " + movie_dict.get(raw_id))
        print("end\n")

    # Question24&25
    print ("Question 24&25 beigns")
    SVD_rmse_range = []
    SVD_mae_range = []
    k_range = range(2, 51, 2)
    min_rmse = 1000.0
    min_mae = 1000.0
    k_min = 0
    for k in k_range:
        algo = SVD(n_factors=k, random_state=0, n_epochs=50)
        dict1 = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=10)
        rmse = sum(dict1['test_rmse']) / 10.0
        mae = sum(dict1['test_mae']) / 10.0
        if (rmse < min_rmse and mae < min_mae):
            min_rmse = rmse
            min_mae = mae
            k_min = k
        SVD_rmse_range.append(rmse)
        SVD_mae_range.append(mae)
    plt.plot(k_range, SVD_rmse_range)
    plt.plot(k_range, SVD_mae_range)
    plt.show()

    print ("minimum k should be " + str(k_min))

    kf = KFold(n_splits=10)
    k_range = range(2, 51, 2)

    # Question26
    print ("Question 26 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = SVD(n_factors=k)
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset = trim_dataset12(testset, 2)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)

    # Question27
    print ("Question 27 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = SVD(n_factors=k)
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset = trim_dataset13(testset)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)

    # Question28
    print ("Question 28 beigns")
    rmse = []
    average_rmse = []
    for k in k_range:
        algo = SVD(n_factors=k)
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            testset = trim_dataset14(testset)
            predictions = algo.test(testset)
            rmse_temp = accuracy.rmse(predictions, verbose=True)
            rmse.append(rmse_temp)
        rmse_average = sum(rmse) / 10.0
        average_rmse.append(rmse_average)
        rmse = []
    plt.plot(k_range, average_rmse)
    plt.show()
    print 'minimum RMSE:'
    print min(average_rmse)

    # question 29: plot roc curve and calculate the auc area
    print ("Question 29 beigns")
    pre_ratings=[]
    act_ratings=[]
    auc_area=[]
    binary_threadhold=[2.5,3,3.5,4]

    trainset, testset = train_test_split(data,test_size=0.1)
    algo = SVD(n_factors=20)

    algo.fit(trainset)
    predictions = algo.test(testset)
    for i in range(len(predictions)):
        act_ratings.append(predictions[i][2])
        pre_ratings.append(predictions[i][3])

    for k in range(len(binary_threadhold)):
        binary_ratings=[]
        for i in range(len(act_ratings)):
            if(act_ratings[i]>=binary_threadhold[k]):
                binary_ratings.append(1)
            else:
                binary_ratings.append(0)
        fpr, tpr, threadhold = metrics.roc_curve(binary_ratings, pre_ratings, pos_label=1)
        auc_score=metrics.auc(fpr, tpr)
        auc_area.append(auc_score)
        print("Auc area is %f with threshold=%s" % (auc_score,str(binary_threadhold[k])))
        plt.figure()
        plt.plot(fpr, tpr)
        plt.title("ROC with threshold=%s" % str(binary_threadhold[k]))
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")

    # Question30
    print ("Question 30 beigns")
    user_rating = []
    userID = 1
    user_average_rating = 0
    total_user_error = 0
    for index in range(len(userIds)):
        if userIds[index] != userID:
            user_average_rating = 1.0 * sum(user_rating) / len(user_rating)
            for rating in user_rating:
                total_user_error = total_user_error + (rating - user_average_rating) ** 2
            total_user_error = total_user_error + (user_average_rating ** 2) * (9066 - len(user_rating))

            userID = userID + 1
            user_rating = []

        user_rating.append(ratings[index])
        user_average_rating = user_average_rating + ratings[index]

    total_user_error = math.sqrt(total_user_error / (671 * 9066))
    print total_user_error

    # Question31
    movie_list = []
    for moive in movieIds:
        if moive not in movie_list:
            movie_list.append(moive)
    rmse_list = []
    for movie_id in movie_list:
        rating_list = []
        for i in range(len(movieIds)):
            if movieIds[i] == movie_id:
                rating_list.append(ratings[i])
        if len(rating_list) > 2:
            mean = np.mean(rating_list)
            mse = 0
            for rating in rating_list:
                mse = mse + (rating - mean) ** 2
            mse = mse + (671 - len(rating_list)) * (mean) ** 2
        rmse_list.append(mse)
    rmse = math.sqrt(sum(rmse_list) / (671 * 9066))
    print ("Question 31 beigns")
    print(rmse)

    # Question32
    movie_list = []
    for moive in movieIds:
        if moive not in movie_list:
            movie_list.append(moive)
    rmse_list = []
    for movie_id in movie_list:
        rating_list = []
        for i in range(len(movieIds)):
            if movieIds[i] == movie_id:
                rating_list.append(ratings[i])
        if len(rating_list) <= 2:
            mean = np.mean(rating_list)
            mse = 0
            for rating in rating_list:
                mse = mse + (rating - mean) ** 2
            mse = mse + (671 - len(rating_list)) * (mean) ** 2
        rmse_list.append(mse)
    rmse = math.sqrt(sum(rmse_list) / (671 * 9066))
    print ("Question 32 beigns")
    print(rmse)

    # Question33
    movie_list = []
    for moive in movieIds:
        if moive not in movie_list:
            movie_list.append(moive)
    rmse_list = []
    for movie_id in movie_list:
        rating_list = []
        for i in range(len(movieIds)):
            if movieIds[i] == movie_id:
                rating_list.append(ratings[i])
        if len(rating_list) >= 5 and np.var(rating_list) >= 2:
            mean = np.mean(rating_list)
            mse = 0
            for rating in rating_list:
                mse = mse + (rating - mean) ** 2
            mse = mse + (671 - len(rating_list)) * (mean) ** 2
        rmse_list.append(mse)
    rmse = math.sqrt(sum(rmse_list) / (671 * 9066))
    print ("Question 33 beigns")
    print(rmse)

    # question 34: plot roc curve and calculate the auc area
    print ("Question 34 beigns")
    pre_ratings_knn=[]
    pre_ratings_nmf=[]
    pre_ratings_mf=[]

    act_ratings=[]
    auc_area=[]
    binary_threadhold=[2.5,3,3.5,4]

    trainset, testset = train_test_split(data,test_size=0.1)


    algo = KNNWithMeans(k=20, sim_options={'name': 'pearson'})
    algo.fit(trainset)
    predictions = algo.test(testset)
    for i in range(len(predictions)):
        act_ratings.append(predictions[i][2])
        pre_ratings_knn.append(predictions[i][3])

    algo = NMF(n_factors=20, random_state=0)
    algo.fit(trainset)
    predictions = algo.test(testset)
    for i in range(len(predictions)):
        pre_ratings_nmf.append(predictions[i][3])

    algo = SVD(n_factors=20)
    algo.fit(trainset)
    predictions = algo.test(testset)
    for i in range(len(predictions)):
        pre_ratings_mf.append(predictions[i][3])

    binary_ratings=[]
    for i in range(len(act_ratings)):
        if(act_ratings[i]>=binary_threadhold[1]):
            binary_ratings.append(1)
        else:
            binary_ratings.append(0)

    fpr_knn, tpr_knn, threadhold_knn = metrics.roc_curve(binary_ratings, pre_ratings_knn, pos_label=1)
    fpr_nmf, tpr_nmf, threadhold_nmf = metrics.roc_curve(binary_ratings, pre_ratings_nmf, pos_label=1)
    fpr_mf, tpr_mf, threadhold_mf = metrics.roc_curve(binary_ratings, pre_ratings_mf, pos_label=1)


    plt.figure()
    plt.plot(fpr_knn, tpr_knn,'r',label='KNN')
    plt.plot(fpr_nmf, tpr_nmf,'b',label='NMF')
    plt.plot(fpr_mf, tpr_mf,'yellow',label='MF')
    plt.legend(loc=4)
    plt.title("ROC with threshold=%s" % str(binary_threadhold[1]))
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()

    # question 36-38
    print ("Question 36-38 beigns")
    def takeFirst(elem):
        return float(elem[0])

    precision_range_knn = []
    recall_range_knn = []
    precision_range_nmf = []
    recall_range_nmf = []
    precision_range_mf = []
    recall_range_mf = []
    t_range = range(1, 26)
    for k in range(3):
        for t in t_range:
            precision_i = 0
            recall_i = 0
            for i in range(10):
                trainset, testset = train_test_split(data, test_size=0.1, random_state=i)
                if (k == 0):
                    algo = KNNWithMeans(k=2, sim_options={'name': 'pearson'})
                elif (k == 1):
                    algo = NMF(n_factors=20, random_state=0)
                else:
                    algo = SVD(n_factors=20)
                algo.fit(trainset)
                predictions = algo.test(testset)

                predictions.sort(key=takeFirst)
                user_recommendation = []
                users_recommendations = []
                user = predictions[0][0]
                for prediction in predictions:
                    if user != prediction[0]:
                        user_recommendation.sort(key=takeFirst)
                        users_recommendations.append(user_recommendation)
                        user_recommendation = []
                        user = prediction[0]
                    user_recommendation.append([-prediction[3], int(prediction[1])])

                testset.sort(key=takeFirst)
                user_groundtruth = []
                users_groundtruthes = []
                user = testset[0][0]
                for test in testset:
                    if user != test[0]:
                        users_groundtruthes.append(user_groundtruth)
                        user_groundtruth = []
                        user = test[0]
                    if test[2] >= 3:
                        user_groundtruth.append(int(test[1]))

                common = 0
                precision_total = 0
                recall_total = 0
                for index in range(len(users_recommendations)):
                    if len(users_groundtruthes[index]) < t:
                        continue
                    precision_total = precision_total + min(t, len(users_recommendations[index]))
                    recall_total = recall_total + len(users_groundtruthes[index])
                    for user_recommendation in users_recommendations[index][
                                               0:min(t, len(users_recommendations[index]))]:
                        if user_recommendation[1] in users_groundtruthes[index]:
                            common = common + 1
                precision_i = precision_i + 1.0 * common / precision_total
                recall_i = recall_i + 1.0 * common / recall_total
            if (k == 0):
                precision_range_knn.append(precision_i / 10.0)
                recall_range_knn.append(recall_i / 10.0)
            elif (k == 1):
                precision_range_nmf.append(precision_i / 10.0)
                recall_range_nmf.append(recall_i / 10.0)
            elif (k == 2):
                precision_range_mf.append(precision_i / 10.0)
                recall_range_mf.append(recall_i / 10.0)

    # plot
    def plotresult(t_range, precision_range, recall_range, title):
        plt.figure()
        plt.plot(t_range, precision_range, label="precision-t", color="red")
        plt.plot(t_range, recall_range, label="recall-t", color="blue")
        plt.legend(loc="best")
        plt.title(title)

        plt.figure()
        plt.plot(recall_range, precision_range)
        plt.xlabel("recall")
        plt.ylabel("precision")
        plt.title(title)
        plt.show()

    print precision_range_knn
    plotresult(t_range, precision_range_knn, recall_range_knn, "KNN predictions")
    plotresult(t_range, precision_range_nmf, recall_range_nmf, "NMF predictions")
    plotresult(t_range, precision_range_mf, recall_range_mf, "MF predictions")

    # question 39
    print ("Question 39 beigns")
    plt.figure()
    plt.plot(recall_range_knn, precision_range_knn, label="knn", color="red")
    plt.plot(recall_range_nmf, precision_range_nmf, label="nmf", color="blue")
    plt.plot(recall_range_mf, precision_range_mf, label="mf", color="green")
    plt.legend(loc="best")
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.show()


def trim_dataset12(testset,k):
    movie_dict={}
    movie_list=[]
    for test_data in testset:
        if test_data[1] not in movie_dict:
            movie_dict.setdefault(test_data[1],1)
        else:
            movie_dict[test_data[1]]+=1
    for key,value in movie_dict.iteritems():
        if value>k:
            movie_list.append(key)


    testset2 = []
    for test_data in testset:
        if test_data[1] in movie_list:
            testset2.append(test_data)                 # remove is not ok?
    return testset2


def trim_dataset13(testset):
    movie_dict={}
    movie_list=[]
    for test_data in testset:
        if test_data[1] not in movie_dict:
            movie_dict.setdefault(test_data[1],1)
        else:
            movie_dict[test_data[1]]+=1
    for key,value in movie_dict.iteritems():
        if value<=2:
            movie_list.append(key)
    testset2=[]
    for test_data in testset:
        if test_data[1] in movie_list:
            testset2.append(test_data)
    return testset2

def trim_dataset14(testset):
    testset=trim_dataset12(testset,5)
    movie_dict = {}
    movie_list = []
    for test_data in testset:
        if test_data[1] not in movie_dict:

            movie_dict.setdefault(test_data[1],[test_data[2]])
        else:
            movie_dict[test_data[1]].append(test_data[2])
    for key, value in movie_dict.iteritems():
        var=np.var(value)
        if var>2:
            movie_list.append(key)
    testset2 = []
    for test_data in testset:
        if test_data[1] in movie_list:
            testset2.append(test_data)
    return testset2

if __name__ == "__main__":
    main()