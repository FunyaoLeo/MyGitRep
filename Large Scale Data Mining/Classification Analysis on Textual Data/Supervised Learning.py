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
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
from string import punctuation
from sklearn.cross_validation import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier


######################################################################
# functions -- Loading Data
######################################################################
def load_and_combine(category_name):
    """
    fetch each category's training data and combine them as one document.
    :param category_name: string, category name
    :return train: a set, contained all the data in a category
            combined_data: string, combined document
    """

    train = fetch_20newsgroups(subset='train', categories=[category_name], shuffle=True, random_state=42)
    combined_data = ''
    for data in train.data:
        combined_data = combined_data + data
    return train, combined_data



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
# functions -- Output and Print
######################################################################
def get_keys(dic, value):
    """
    return key of corrponding values
    :param dic: dictionary, containing key-value pair
    :param value: int, value of dictionary
    :return: key: string, key stored in the dictionary
    """
    return [k for k, v in dic.iteritems() if v == value]

def significant_words(category_name, k, tficf_array, vectorizer):
    categories = ['rec.motorcycles', 'comp.sys.mac.hardware', 'talk.politics.misc',
                  'soc.religion.christian', 'comp.graphics', 'sci.med', 'talk.religion.misc',
                  'comp.windows.x', 'comp.sys.ibm.pc.hardware', 'talk.politics.guns', 'alt.atheism',
                  'comp.os.ms-windows.misc', 'sci.crypt', 'sci.space', 'misc.forsale',
                  'rec.sport.hockey', 'rec.sport.baseball', 'sci.electronics', 'rec.autos', 'talk.politics.mideast']
    category_dic = {}
    index = 0
    for category in categories:
        category_dic[category] = index
        index = index+1
    index = category_dic.get(category_name)

    max_value = [0 for x in range(k)]
    max_index = [0 for x in range(k)]
    for top in range(k):
        max_value[top] = tficf_array[index][0]
        max_index[top] = 0
        for freq_index in range(1, len(tficf_array[0])):
            if tficf_array[index][freq_index] > max_value[top]:
                max_value[top] = tficf_array[index][freq_index]
                max_index[top] = freq_index
        tficf_array[index][max_index[top]] = -1
    print("top " + str(k) + "words in category " + category_name + ":")
    for top in range(k):
        print(get_keys(vectorizer.vocabulary_, max_index[top]))
    print("\n")

def plot_roc(fpr, tpr, label_):
    """
    plot roc curve of different classifer
    :param fpr: false positive rate
    :param tpr: true positive rate
    :param label: string, label on the plot
    :return:
    """
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange',lw=2, label='ROC curve ')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([-0.1, 1.1])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=15)
    plt.ylabel('True Positive Rate', fontsize=15)
    plt.title('ROC curve of  min_df=2, '+label_)
    plt.show()

def performance(y_true, y_pred, y_prob, plot_label):
    """
    Calculates the performance metric based on the agreement between the
    true labels and the predicted labels.
    :param y_true: numpy array of shape (n,), known labels
    :param y_pred: y_pred -- numpy array of shape (n,), (continuous-valued) predictions
    :param y_prob: array, probabily of test set
    :param plot_label: string, label on the plot
    :return:
    """
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_prob[:, 1])
    confusion = metrics.confusion_matrix(y_true, y_pred)
    TN, FP = confusion[0, 0], confusion[0, 1]
    FN, TP = confusion[1, 0], confusion[1, 1]

    plot_roc(fpr=fpr, tpr=tpr, label_=plot_label)
    print ("Confusion Matrix is: ")
    print(confusion)
    print ("Accuracy is :" + str(metrics.accuracy_score(y_true, y_pred)))
    print ("Recall is :" + str(metrics.recall_score(y_true, y_pred)))
    print("Precision is :" + str(metrics.precision_score(y_true, y_pred))+"\n")

def find_optimum_c(train_array, train_result, test_array, test_result):
    """
    from range c=[10^-3, 10^3], find optimum c that returns highest accuracy
    :param train_array: array, training input array
    :param train_result: array, training result array
    :param test_array: array, testing input array
    :param test_result: array, testinging result array
    :return: optimum c
    """
    C_range = 10.0 ** np.arange(-3, 4)
    max_perf = 0
    optimum_c = 0
    for c in C_range:
        clf = SVC(C=c, probability=True)
        clf.fit(train_array, train_result)
        test_predict = clf.predict(test_array)
        perf = metrics.accuracy_score(test_result, test_predict)
        print perf
        print c
        if perf > max_perf:
            max_perf = perf
            optimum_c = c
    return optimum_c





######################################################################
# functions -- Decreasing Dimensions
######################################################################
def SVD_downsize(array_train, array_test, k):
    """
    Utilize SVD method to extract top k eigenvalue and downsize matrix into dimension k
    :param array_train: array, array used for training
    :param array_test: array, array used for testing
    :param k: int, number of top eigenvalues to keep
    :return: downsized training_array and test array
    """
    model = TruncatedSVD(n_components=k, random_state=0)
    svd_train = model.fit_transform(array_train.transpose())
    svd_test = model.transform(array_test.transpose())
    return svd_train, svd_test

def NMF_downsize(array_train, array_test, k):
    """
    Utilize NMF method to downsize matrix into dimension k
    :param array_train: array, array used for training
    :param array_test: array, array used for testing
    :param k: int, number of top eigenvalues to keep
    :return: downsized training_array and test array
    """
    model = NMF(n_components=50, init='random', random_state=0)
    W_train = model.fit_transform(array_train.transpose())
    print(array_train.shape)
    print len(W_train)
    print len(W_train[0])
    W_test = model.transform(array_test.transpose())
    print(array_test.shape)
    print len(W_test)
    print len(W_test[0])
    return W_train, W_test



######################################################################
# functions -- Model Training and Performance
######################################################################
def SVM_performance(train_array, train_result, test_array, test_result, c):
    """
    train SVD model and print the performance
    :param train_array: array, training input array
    :param train_result: array, training result array
    :param test_array: array, testing input array
    :param test_result: array, testing result array
    :param c: int, penalty parameter for svm
    :return:
    """
    clf = SVC(C=c, probability=True, random_state=42)
    clf.fit(train_array, train_result)

    test_predict = clf.predict(test_array)
    test_score = clf.predict_proba(test_array)

    performance(y_true=test_result, y_pred=test_predict, y_prob=test_score,
                plot_label="C = " + str(c))

def naive_bayes_performance(train_array, train_result, test_array, test_result, label):
    """
    train naive_bayes model and print the performance
    :param train_array: array, training input array
    :param train_result: array, training result array
    :param test_array: array, testing input array
    :param test_result: array, testing result array
    :param label: string, label for the plot
    :return:
    """
    clf = MultinomialNB()
    clf.fit(train_array, train_result)

    naive_Bayes_pred = clf.predict(test_array)
    naive_Bayes_score = clf.predict_proba(test_array)

    performance(test_result, naive_Bayes_pred, naive_Bayes_score, "naive bayes for "+label)

def logistics_performance(train_array, train_result, test_array,test_result, label):
    """
    train logistics model and print the performance
    :param train_array: array, training input array
    :param train_result: array, training result array
    :param test_array: array, testing input array
    :param test_result: array, testing result array
    :param label: string, label for the plot
    :return:
    """
    clf = LogisticRegression()
    clf.fit(train_array, train_result)

    logistics_pred = clf.predict(test_array)
    logistics_score = clf.predict_proba(test_array)

    performance(test_result, logistics_pred, logistics_score, "logistics for " + label)



######################################################################
# main
######################################################################
def main():

    # Loading data of all the categories and store it into the dictionary
    categories = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
                  'comp.sys.mac.hardware', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                  'rec.sport.hockey', 'misc.forsale', 'soc.religion.christian', 'alt.atheism',
                  'comp.windows.x', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space',
                  'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']
    print len(fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42).target)


    # Empty dictionaries, newsgroup_data for data of each news group,
    # combined_documents for combined documents of each category.
    # Keys are category string, values are stored data

    newsgroup_data = {}
    combined_documents = {}

    # Load data into corresponding dictionaries
    for category in categories:
        train, combined_data = load_and_combine(category)
        newsgroup_data[category] = train
        combined_documents[category] = combined_data

    # part a:  plot the histogram of data numbers
    categories_a_needed = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
                  'comp.sys.mac.hardware', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                  'rec.sport.hockey']

    # Get number of each categories and make a list
    nums = []
    for category in categories_a_needed:
        nums.append(newsgroup_data.get(category).target.shape[0])
        
    labels = ['Graphics', 'Misc', 'PCHardware', 'MacHardware', 'Autos',
              'Motorcycles', 'Baseball', 'Hockey']
    plt.bar(range(len(nums)), nums, tick_label=labels)
    plt.show()


    # part b: tokenize data and using TFIDF to measure the term frequencies
    text_train = fetch_20newsgroups(subset='train', categories=categories_a_needed, shuffle=True, random_state=42)
    text_test = fetch_20newsgroups(subset='test', categories=categories_a_needed, shuffle=True, random_state=42)

    tfidf_array_2, tfidf_array_2_test, vectorizer_2 = vectorize_text_array(text_array_train=text_train.data, text_array_test=text_test.data, min_df=2, max_df=0.7)
    tfidf_array_5, tfidf_array_5_test, vectorizer_5 = vectorize_text_array(text_array_train=text_train.data, text_array_test=text_test.data, min_df=5, max_df=0.7)
    tfidf_array_2 = tfidf_array_2.transpose()
    tfidf_array_2_test = tfidf_array_2_test.transpose()
    tfidf_array_5 = tfidf_array_5.transpose()
    tfidf_array_5_test = tfidf_array_5_test.transpose()

    # part c: find the 10 most significant terms in each classes
    word_list = []
    for category, combined_document in combined_documents.iteritems():
        word_list.append(combined_document)
    tficf_array, tficf_array_test, vectorizer_significant = vectorize_text_array(text_array_train=word_list, text_array_test=word_list, min_df=2, max_df=18)
    tficf_array = tficf_array.toarray()

    significant_words(category_name='comp.sys.ibm.pc.hardware', k=10, tficf_array=tficf_array, vectorizer=vectorizer_significant)
    significant_words(category_name='comp.sys.mac.hardware', k=10, tficf_array=tficf_array, vectorizer=vectorizer_significant)
    significant_words(category_name='misc.forsale', k=10, tficf_array=tficf_array, vectorizer=vectorizer_significant)
    significant_words(category_name='soc.religion.christian', k=10, tficf_array=tficf_array, vectorizer=vectorizer_significant)


    # part d: decrease the dimension of the tfidf matrix
    # SVD method
    SVD_tfidf_2_train, SVD_tfidf_2_test = SVD_downsize(array_train=tfidf_array_2, array_test=tfidf_array_2_test, k=50)
    SVD_tfidf_5_train, SVD_tfidf_5_test = SVD_downsize(array_train=tfidf_array_5, array_test=tfidf_array_5_test, k=50)

    # NMF method
    NMF_tfidf_2_train, NMF_tfidf_2_test= NMF_downsize(array_train=tfidf_array_2, array_test=tfidf_array_2_test, k=50)
    NMF_tfidf_5_train, NMF_tfidf_5_test = NMF_downsize(array_train=tfidf_array_5, array_test=tfidf_array_5_test, k=50)


    # part e: Support Vector Machine Classifier
    train_result = shrink_classes(results=text_train.target)
    test_result = shrink_classes(results=text_test.target)

    kf = StratifiedKFold(train_result, n_folds=5)

    print("\nmin_df = 2, C = 1000")
    SVM_performance(train_array=NMF_tfidf_2_train, train_result=train_result, test_array=NMF_tfidf_2_test,
                    test_result=test_result, c=1000)
                    
    print("\nmin_df = 2, C = 0.001")
    SVM_performance(train_array=NMF_tfidf_2_train, train_result=train_result, test_array=NMF_tfidf_2_test,
                    test_result=test_result, c=0.001)

    print("\nmin_df = 2, C = 0.001")
    SVM_performance(train_array=NMF_tfidf_2_train, train_result=train_result, test_array=NMF_tfidf_2_test,
                    test_result=test_result, c=0.001)

    print("\nmin_df = 2, C = 0.001")
    SVM_performance(train_array=NMF_tfidf_2_train, train_result=train_result, test_array=NMF_tfidf_2_test,
                    test_result=test_result, c=0.001)

    print("\nmin_df = 5, C = 1000")
    SVM_performance(train_array=SVD_tfidf_5_train, train_result=train_result, test_array=SVD_tfidf_5_test,
                    test_result=test_result, c=1000)

    print("min_df = 5, C = 0.001")
    SVM_performance(train_array=SVD_tfidf_5_train, train_result=train_result, test_array=SVD_tfidf_5_test,
                    test_result=test_result, c=0.001)


    # part f Cross-Validation to find maximum c

    kf = StratifiedKFold(train_result, n_folds=5)

    print("For min_df=2: ")
    for train_index, validation_index in kf:
        svd_train_2_fold, svd_train_validation = SVD_tfidf_2_train[train_index], SVD_tfidf_2_train[validation_index]
        train_result_2_fold, train_result_validation = train_result[train_index], train_result[validation_index]

    optimum_c = find_optimum_c(train_array=svd_train_2_fold, train_result=train_result_2_fold,
                               test_array=svd_train_validation, test_result=train_result_validation)
    SVM_performance(train_array=SVD_tfidf_2_train, train_result=train_result, test_array=SVD_tfidf_2_test,
                    test_result=test_result, c=optimum_c)
    

    print("For min_df=5: ")
    for train_index, validation_index in kf:
        svd_train_5_fold, svd_train_validation = SVD_tfidf_5_train[train_index], SVD_tfidf_5_train[validation_index]
        train_result_5_fold, train_result_validation = train_result[train_index], train_result[validation_index]

    optimum_c = find_optimum_c(train_array=svd_train_5_fold, train_result=train_result_5_fold,
                               test_array=svd_train_validation, test_result=train_result_validation)

    SVM_performance(train_array=SVD_tfidf_5_train, train_result=train_result, test_array=SVD_tfidf_5_test,
                    test_result=test_result, c=optimum_c)

    # part g: naive Bayes classifier
    print("naive bayes for min_df = 2")
    naive_bayes_performance(train_array=NMF_tfidf_2_train, train_result=train_result, test_array=NMF_tfidf_2_test,
                            test_result=test_result, label="min_df=2")

    print("naive bayes for min_df = 5")
    naive_bayes_performance(train_array=NMF_tfidf_5_train, train_result=train_result, test_array=NMF_tfidf_5_test,
                            test_result=test_result, label="min_df=5")

    
    # part h: logistic Regression
    print("logistics for min_df = 2")
    logistics_performance(train_array=SVD_tfidf_2_train, train_result=train_result, test_array=SVD_tfidf_2_test,
                            test_result=test_result, label="min_df=2")

    print("logistics for min_df = 5")
    logistics_performance(train_array=SVD_tfidf_5_train, train_result=train_result, test_array=SVD_tfidf_5_test,
                            test_result=test_result, label="min_df=5")


    # part i: sweep through parameter
    print("For min_df=2")
    C_range = 10.0 ** np.arange(-3, 3)
    print("For l1 penalty")
    for c in C_range:
        clf = LogisticRegression(penalty='l1', C=c)
        clf.fit(NMF_tfidf_2_train, train_result)
        test_predict = clf.predict(NMF_tfidf_2_test)
        print ("Accuracy is :" + str(metrics.accuracy_score(test_result, test_predict)) + " for c = " + str(c))
        print("Coefficients of hyperplane :" + str(clf.coef_) + " for c = " + str(c))

    print("\n\n\n\n\n\n\nFor l2 penalty")
    for c in C_range:
        clf_l2 = LogisticRegression(penalty='l2', C=c)
        clf_l2.fit(NMF_tfidf_2_train, train_result)
        test_predict_2 = clf.predict(NMF_tfidf_2_test)
        print ("Accuracy is :" + str(metrics.accuracy_score(test_result, test_predict_2)) + " for c = " + str(c))
        print("Coefficients of hyperplane :" + str(clf_l2.coef_) + " for c = " + str(c))

    print("For min_df=2")
    C_range = 10.0 ** np.arange(-3, 3)
    print("For l1 penalty")
    for c in C_range:
        clf = LogisticRegression(penalty='l1', C=c)
        clf.fit(SVD_tfidf_2_train, train_result)
        test_predict = clf.predict(SVD_tfidf_2_test)
        print ("Accuracy is :" + str(metrics.accuracy_score(test_result, test_predict)) + " for c = " + str(c))
        print("Coefficients of hyperplane :" + str(clf.coef_) + " for c = " + str(c))

    print("\n\n\n\n\n\n\nFor l2 penalty")
    for c in C_range:
        clf_l2 = LogisticRegression(penalty='l2', C=c)
        clf_l2.fit(SVD_tfidf_2_train, train_result)
        test_predict_2 = clf.predict(SVD_tfidf_2_test)
        print ("Accuracy is :" + str(metrics.accuracy_score(test_result, test_predict_2)) + " for c = " + str(c))
        print("Coefficients of hyperplane :" + str(clf_l2.coef_) + " for c = " + str(c))

    print("\n\n\n\n\n\n\nFor min_df=5")
    C_range = 10.0 ** np.arange(-3, 3)
    print("For l1 penalty")
    for c in C_range:
        clf = LogisticRegression(penalty='l1', C=c)
        clf.fit(SVD_tfidf_5_train, train_result)
        test_predict = clf.predict(SVD_tfidf_5_test)
        print ("Accuracy is :" + str(metrics.accuracy_score(test_result, test_predict)) + " for c = " + str(c))
        print("Coefficients of hyperplane :" + str(clf.coef_) + " for c = " + str(c))

    print("\n\n\n\n\n\n\nFor l2 penalty")
    for c in C_range:
        clf_l2 = LogisticRegression(penalty='l2', C=c)
        clf_l2.fit(SVD_tfidf_5_train, train_result)
        test_predict_5 = clf.predict(SVD_tfidf_5_test)
        print ("Accuracy is :" + str(metrics.accuracy_score(test_result, test_predict_5)) + " for c = " + str(c))
        print("Coefficients of hyperplane :" + str(clf_l2.coef_) + " for c = " + str(c))


    # part i': multiclass classification
    categories_i_needed = ['comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'misc.forsale',
                           'soc.religion.christian']
    text_train = fetch_20newsgroups(subset='train', categories=categories_i_needed, shuffle=True, random_state=42)
    text_test = fetch_20newsgroups(subset='test', categories=categories_i_needed, shuffle=True, random_state=42)

    tfidf_array_2, tfidf_array_2_test, vectorizer_2 = vectorize_text_array(text_array_train=text_train.data,
                                                                           text_array_test=text_test.data, min_df=2,
                                                                           max_df=0.7)
    tfidf_array_2 = tfidf_array_2.transpose()
    tfidf_array_2_test = tfidf_array_2_test.transpose()
    SVD_tfidf_2_train, SVD_tfidf_2_test = SVD_downsize(array_train=tfidf_array_2, array_test=tfidf_array_2_test, k=50)
    NMF_tfidf_2_train, NMF_tfidf_2_test = NMF_downsize(array_train=tfidf_array_2, array_test=tfidf_array_2_test, k=50)
    train_result = text_train.target
    test_result = text_test.target

    clf = MultinomialNB()
    clf.fit(NMF_tfidf_2_train, train_result)
    naive_Bayes_multi_pred = clf.predict(NMF_tfidf_2_test)
    print ("Confusion Matrix is: ")
    print(metrics.confusion_matrix(test_result, naive_Bayes_multi_pred))
    print ("Accuracy is :" + str(metrics.accuracy_score(test_result, naive_Bayes_multi_pred)))
    print ("Recall is :" + str(metrics.recall_score(test_result, naive_Bayes_multi_pred, average='weighted')))
    print("Precision is :" + str(metrics.precision_score(test_result, naive_Bayes_multi_pred, average='weighted')) + "\n")

    print("one vs one svm, LSI")
    clf = SVC(C=1000, decision_function_shape='ovo')
    clf.fit(SVD_tfidf_2_train, train_result)
    svc_pred = clf.predict(SVD_tfidf_2_test)
    print ("Confusion Matrix is: ")
    print(metrics.confusion_matrix(test_result, svc_pred))
    print ("Accuracy is :" + str(metrics.accuracy_score(test_result, svc_pred)))
    print ("Recall is :" + str(metrics.recall_score(test_result, svc_pred, average='weighted')))
    print("Precision is :" + str(metrics.precision_score(test_result, svc_pred, average='weighted')) + "\n")



if __name__ == "__main__" :
    main()









