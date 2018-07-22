"""
Author      : Fangyao Liu
Description : 20 news group topic classification
"""
import numpy as np
import scipy
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import NMF
from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from string import punctuation

######################################################################
# functions -- Processing Text Array
######################################################################
def vectorize_text_array(text_array_train, text_array_test,  min_df, max_df=1.0):
    """
    Stem words first, then vectorize text array and transfer it into a tfidf array
    :param text_array: array, text array
           min_df: int, lowest frequency that a word has to appear in a document
    :return: tfidf_array: array, transform text array into a frequency array using TF-IDF
             vectorizer: countevectorizer, an instance of countvectorizer
    """

    stop_words = text.ENGLISH_STOP_WORDS
    stop_words_en = stopwords.words('english')
    combined_stopwords = set.union(set(stop_words_en), set(punctuation), set(stop_words))

    vectorizer = CountVectorizer(stop_words=combined_stopwords, min_df=min_df, max_df=max_df)
    text_array_train = vectorizer.fit_transform(text_array_train)
    text_array_test = vectorizer.transform(text_array_test)

    tfidf_transformer = TfidfTransformer(smooth_idf=False)
    tfidf_array_train = tfidf_transformer.fit_transform(text_array_train)
    tfidf_array_test = tfidf_transformer.transform(text_array_test)

    return tfidf_array_train, tfidf_array_test, vectorizer

def shrink_classes(results):
    """
    Combine some classes into one and shrink the class size to 2
    :param results: array, containing labels
    :return: numpy array, shrinked label array
    """
    train_result = []
    for result in results:
        if result <= 3:
            train_result.append(0)
        else:
            train_result.append(1)

    return np.array(train_result)



######################################################################
# functions -- Decreasing Dimensions
######################################################################
def SVD_downsize(array_train, array_test, k):
    """
    Utilize SVD method to extract top k eigenvalue and downsize matrix into dimension k
    :param array_train: array, array used for training
    :param array_test: array, array used for testing
    :param k: int, number of top eigenvalues to keep
    :return: downsized training_array, testing_array and training model
    """
    model = TruncatedSVD(n_components=k, random_state=0)
    svd_train = model.fit_transform(array_train)
    svd_test = model.transform(array_test)
    return svd_train, svd_test, model

def NMF_downsize(array_train, array_test, k):
    """
    Utilize NMF method to downsize matrix into dimension k
    :param array_train: array, array used for training
    :param array_test: array, array used for testing
    :param k: int, number of top eigenvalues to keep
    :return: downsized training_array and test array
    """
    model = NMF(n_components=k, init='random', random_state=0)
    W_train = model.fit_transform(array_train)
    W_test = model.transform(array_test)
    return W_train, W_test



######################################################################
# functions -- Output and Print
######################################################################
def performance(y_true, y_pred):
    """
    Calculates the performance metric based on the agreement between the
    true labels and the predicted labels.
    :param y_true: numpy array of shape (n,), known labels
    :param y_pred: y_pred -- numpy array of shape (n,), (continuous-valued) predictions
    :param y_prob: array, probabily of test set
    :return:
    """
    confusion = metrics.confusion_matrix(y_true, y_pred)
    TN, FP = confusion[0, 0], confusion[0, 1]
    FN, TP = confusion[1, 0], confusion[1, 1]

    print ("Confusion Matrix is: ")
    print(confusion)

    print ("Homogeneity score is :" + str(metrics.homogeneity_score(y_true, y_pred)))
    print ("Completeness score is :" + str(metrics.completeness_score(y_true, y_pred)))
    print ("V measure score is :" + str(metrics.v_measure_score(y_true, y_pred)))
    print ("Adjusted rand score is :" + str(metrics.adjusted_rand_score(y_true, y_pred)))
    print ("Adjusted mutual info score is :" + str(metrics.adjusted_mutual_info_score(y_true, y_pred)))

def percent_of_variance(singular_values):
    """
    This function taks singular values of TF_IDF matrix and plot the
    percentage of variance vs the number of top singular values we
    take.
    :param singular_values:
    :return: percentage of variance plot
    """
    sum_singular_values = np.ndarray.sum(singular_values ** 2)
    print len(singular_values)
    print singular_values
    print sum_singular_values
    r_collection = []
    percent_of_variance = []
    r = 1
    sum_of_variance = 0
    for sigma in singular_values:
        r_collection.append(r)
        sum_of_variance = sum_of_variance + sigma * sigma
        percent_of_variance.append(sum_of_variance * 1.0 / sum_singular_values)
        if (r == 1000):
            break
        else:
            r = r + 1
    plt.plot(r_collection, percent_of_variance)
    plt.title("perceent of variance from top 1 to 1000")
    plt.show()

def performance_plot(training_array, testing_array, train_result, method, clusters):
    """
    sweeping r from 1 to 300, find out best dimension of variables for K-clustering
    by ploting the performance plot
    :param training_array: a tf-idf array, training matrix
    :param testing_array: a tf-idf array, testing array
    :param train_result: one dimension array, training label
    :param method: int,  method of different factorization. 0 represents SVD, 1 represents NMF
    :param clusters: int, number of clusters
    :return: performance plot
    """
    Homogeneity = []
    Completeness = []
    V_measure = []
    Adjusted_rand = []
    Adjusted_mutual_info = []

    r_range = [1, 2, 3, 5, 10, 20, 50, 100, 300]
    for r in r_range:
        if(method==0):
            fac_tfidf_3_train, fac_tfidf_3_test, fac_model = SVD_downsize(array_train=training_array,
                                                                      array_test=testing_array, k=r)
        elif(method==1):
            fac_tfidf_3_train, fac_tfidf_3_test = NMF_downsize(array_train=training_array,
                                                               array_test=testing_array,
                                                               k=r)
        clf = KMeans(n_clusters=clusters, random_state=0)
        clf.fit(fac_tfidf_3_train)
        train_predict = clf.labels_
        Homogeneity.append(metrics.homogeneity_score(train_result, train_predict))
        Completeness.append(metrics.completeness_score(train_result, train_predict))
        V_measure.append(metrics.v_measure_score(train_result, train_predict))
        Adjusted_rand.append(metrics.adjusted_rand_score(train_result, train_predict))
        Adjusted_mutual_info.append(metrics.adjusted_mutual_info_score(train_result, train_predict))

    plt.plot(r_range, Homogeneity, color='r', label='Homogeneity')
    plt.plot(r_range, Completeness, color='y', label='Completeness')
    plt.plot(r_range, V_measure, color='g', label='V_measure')
    plt.plot(r_range, Adjusted_rand, color='b', label='Adjusted_rand')
    plt.plot(r_range, Adjusted_mutual_info, color='m', label='Adjusted_mutual_info')
    plt.legend(loc='lower right')
    print("Homogeneity")
    print(Homogeneity)
    print("adjusted_mutual_info")
    print(Adjusted_mutual_info)
    print("adjusted_rand")
    print(Adjusted_rand)
    print("V measure")
    print(V_measure)
    print("Completeness")
    print(Completeness)
    if (method == 0):
        plt.title("Metrics Plot for SVD")
    elif(method==1):
        plt.title("Metrics Plot for NMF")
    plt.show()



def main():

    #part a Building TF-IDf matrix, min_df=3
    categories_a_needed = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
                           'comp.sys.mac.hardware', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                           'rec.sport.hockey']

    text_train = fetch_20newsgroups(subset='train', categories=categories_a_needed, shuffle=True, random_state=42)
    text_test = fetch_20newsgroups(subset='test', categories=categories_a_needed, shuffle=True, random_state=42)
    tfidf_array_3_train, tfidf_array_3_test, vectorizer_3 = vectorize_text_array(text_array_train=text_train.data,
                                                                           text_array_test=text_test.data, min_df=3,
                                                                           max_df=0.7)
    print("Size of the TF-IDF matrix is: " + str(tfidf_array_3_train.shape))

    #part b: high dimension clustering
    train_result = shrink_classes(results=text_train.target)

    clf = KMeans(n_clusters=2, random_state=0).fit(tfidf_array_3_train)
    train_predict = clf.labels_
    performance(train_result, train_predict)
    

    #part c1: LSI exploration

    SVD_tfidf_3_train, SVD_tfidf_3_test, SVD_model = SVD_downsize(array_train=tfidf_array_3_train, array_test=tfidf_array_3_test, k=min(tfidf_array_3_train.shape))
    percent_of_variance(SVD_model.singular_values_)
    
    #part c2: explore best r
    performance_plot(training_array=tfidf_array_3_train, testing_array=tfidf_array_3_test, train_result=train_result,
                     method=0, clusters=2)
    performance_plot(training_array=tfidf_array_3_train, testing_array=tfidf_array_3_test, train_result=train_result,
                     method=1,clusters=2)
    

    #part 4a: visualize the data
    SVD_tfidf_3_train, SVD_tfidf_3_test, SVD_model = SVD_downsize(array_train=tfidf_array_3_train,
                                                                  array_test=tfidf_array_3_test, k=2)
    print("clustering result for SVD")
    clf = KMeans(n_clusters=2, random_state=0)
    clf.fit(SVD_tfidf_3_train)
    train_predict = clf.labels_
    performance(train_result, train_predict)
    plt.scatter(x=SVD_tfidf_3_train[:, 0], y=SVD_tfidf_3_train[:, 1], c=train_predict)
    plt.title("clustering result for SVD")
    plt.show()

    NMF_tfidf_3_train, NMF_tfidf_3_test = NMF_downsize(array_train=tfidf_array_3_train,
                                                       array_test=tfidf_array_3_test,
                                                       k=2)
    print("clustering result for NMF")
    clf = KMeans(n_clusters=2, random_state=0)
    clf.fit(NMF_tfidf_3_train)
    train_predict = clf.labels_
    performance(train_result, train_predict)
    plt.scatter(x=NMF_tfidf_3_train[:, 0], y=NMF_tfidf_3_train[:, 1], c=train_predict)
    plt.title("clustering result for NMF")
    plt.show()

    #part 4b: preprocess the data
    # unit variance
    print("normalized clustering result for SVD")
    SVD_scaled = preprocessing.scale(SVD_tfidf_3_train)
    clf = KMeans(n_clusters=2, random_state=0)
    clf.fit(SVD_scaled)
    train_predict = clf.labels_
    performance(train_result, train_predict)
    plt.scatter(x=SVD_scaled[:, 0], y=SVD_scaled[:, 1], c=train_predict)
    plt.title("normalized clustering result for SVD")
    plt.show()

    print("normalized clustering result for NMF")
    NMF_scaled = preprocessing.scale(NMF_tfidf_3_train)
    clf = KMeans(n_clusters=2, random_state=0)
    clf.fit(NMF_scaled)
    train_predict = clf.labels_
    performance(train_result, train_predict)
    plt.scatter(x=NMF_scaled[:, 0], y=NMF_scaled[:, 1], c=train_predict)
    plt.title("normalized clustering result for NMF")
    plt.show()









    #part 5: 20 groups exploration
    categories = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
                  'comp.sys.mac.hardware', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                  'rec.sport.hockey', 'misc.forsale', 'soc.religion.christian', 'alt.atheism',
                  'comp.windows.x', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space',
                  'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']

    text_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
    text_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)
    tfidf_array_3_train, tfidf_array_3_test, vectorizer_3 = vectorize_text_array(text_array_train=text_train.data,
                                                                                 text_array_test=text_test.data,
                                                                                 min_df=3,
                                                                                 max_df=0.7)
    train_result = text_train.target

    """
    performance_plot(training_array=tfidf_array_3_train, testing_array=tfidf_array_3_test, train_result=train_result,
                     method=0, clusters=20)

    performance_plot(training_array=tfidf_array_3_train, testing_array=tfidf_array_3_test, train_result=train_result,
                     method=1, clusters=20)
    """
    SVD_tfidf_3_train, SVD_tfidf_3_test, SVD_model = SVD_downsize(array_train=tfidf_array_3_train,
                                                                  array_test=tfidf_array_3_test, k=50)
    print("clustering result for SVD")
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(SVD_tfidf_3_train)
    train_predict = clf.labels_
    performance(train_result, train_predict)


    NMF_tfidf_3_train, NMF_tfidf_3_test = NMF_downsize(array_train=tfidf_array_3_train,
                                                       array_test=tfidf_array_3_test,
                                                       k=20)
    print("clustering result for NMF")
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(NMF_tfidf_3_train)
    train_predict = clf.labels_
    performance(train_result, train_predict)

    # part 4b: preprocess the data
    # unit variance
    print("normalized clustering result for SVD")
    SVD_scaled = preprocessing.scale(SVD_tfidf_3_train)
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(SVD_scaled)
    train_predict = clf.labels_
    performance(train_result, train_predict)

    print("normalized clustering result for NMF")
    NMF_scaled = preprocessing.scale(NMF_tfidf_3_train)
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(NMF_scaled)
    train_predict = clf.labels_
    performance(train_result, train_predict)


    print("nonlinear transform clustering result for NMF")
    NMF_log = np.log(NMF_tfidf_3_train + 1)
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(NMF_log)
    train_predict = clf.labels_
    performance(train_result, train_predict)


    print("nonlinear transform and normalize clustering result for NMF")
    NMF_log = np.log(NMF_tfidf_3_train + 1)
    NMF_scaled = preprocessing.scale(NMF_log)
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(NMF_scaled)
    train_predict = clf.labels_
    performance(train_result, train_predict)


    print("normalize and nonlinear transform clustering result for NMF")
    NMF_scaled = preprocessing.scale(NMF_tfidf_3_train)
    NMF_log = np.log(NMF_scaled + 1 - NMF_scaled.min())
    clf = KMeans(n_clusters=20, random_state=0)
    clf.fit(NMF_log)
    train_predict = clf.labels_
    performance(train_result, train_predict)











if __name__ == "__main__" :
    main()