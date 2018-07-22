"""
Author      : Yi-Chieh Wu, Sriram Sankararman
Description : Twitter
"""

from string import punctuation

import numpy as np

# !!! MAKE SURE TO USE SVC.decision_function(X), NOT SVC.predict(X) !!!
# (this makes ``continuous-valued'' predictions)
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn import metrics

######################################################################
# functions -- input/output
######################################################################

def read_vector_file(fname):
    """
    Reads and returns a vector from a file.
    
    Parameters
    --------------------
        fname  -- string, filename
        
    Returns
    --------------------
        labels -- numpy array of shape (n,)
                    n is the number of non-blank lines in the text file
    """
    return np.genfromtxt(fname)


def write_label_answer(vec, outfile):
    """
    Writes your label vector to the given file.
    
    Parameters
    --------------------
        vec     -- numpy array of shape (n,) or (n,1), predicted scores
        outfile -- string, output filename
    """
    
    # for this project, you should predict 70 labels
    if(vec.shape[0] != 70):
        print("Error - output vector should have 70 rows.")
        print("Aborting write.")
        return
    
    np.savetxt(outfile, vec)    


######################################################################
# functions -- feature extraction
######################################################################

def extract_words(input_string):
    """
    Processes the input_string, separating it into "words" based on the presence
    of spaces, and separating punctuation marks into their own words.
    
    Parameters
    --------------------
        input_string -- string of characters
    
    Returns
    --------------------
        words        -- list of lowercase "words"
    """
    
    for c in punctuation :
        input_string = input_string.replace(c, ' ' + c + ' ')
    return input_string.lower().split()


def extract_dictionary(infile):
    """
    Given a filename, reads the text file and builds a dictionary of unique
    words/punctuations.

    Parameters
    --------------------
        infile    -- string, filename

    Returns
    --------------------
        word_list -- dictionary, (key, value) pairs are (word, index)
    """

    word_list = {}
    key = 0
    with open(infile, 'rU') as fid :
        ### ========== TODO : START ========== ###
        # part 1a: process each line to populate word_list
        for line in fid:
            word_list_temp = extract_words(line)
            for word in word_list_temp:
                if word not in word_list:
                    word_list[word] = key
                    key += 1
        ### ========== TODO : END ========== ###
    print word_list
    return word_list


def extract_feature_vectors(infile, word_list):
    """
    Produces a bag-of-words representation of a text file specified by the
    filename infile based on the dictionary word_list.

    Parameters
    --------------------
        infile         -- string, filename
        word_list      -- dictionary, (key, value) pairs are (word, index)

    Returns
    --------------------
        feature_matrix -- numpy array of shape (n,d)
                          boolean (0,1) array indicating word presence in a string
                            n is the number of non-blank lines in the text file
                            d is the number of unique words in the text file
    """

    num_lines = sum(1 for line in open(infile,'rU'))
    num_words = len(word_list)
    feature_matrix = np.zeros((num_lines, num_words))

    with open(infile, 'rU') as fid :
        ### ========== TODO : START ========== ###
        # part 1b: process each line to populate feature_matrix
        i = 0;
        for line in fid:
            line_temp = extract_words(line)
            for word in line_temp:
                feature_matrix[i][word_list[word]] = 1
            i = i+1
        ### ========== TODO : END ========== ###
    return feature_matrix


######################################################################
# functions -- evaluation
######################################################################

def performance(y_true, y_pred, metric="accuracy"):
    """
    Calculates the performance metric based on the agreement between the
    true labels and the predicted labels.

    Parameters
    --------------------
        y_true -- numpy array of shape (n,), known labels
        y_pred -- numpy array of shape (n,), (continuous-valued) predictions
        metric -- string, option used to select the performance measure
                  options: 'accuracy', 'f1-score', 'auroc', 'precision',
                           'sensitivity', 'specificity'

    Returns
    --------------------
        score  -- float, performance score
    """
    # map continuous-valued predictions to binary labels
    y_label = np.sign(y_pred)
    y_label[y_label==0] = 1

    ### ========== TODO : START ========== ###
    # part 2a: compute classifier performance
    score = 0
    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_label).ravel()
    if metric == "accuracy":
        score = metrics.accuracy_score(y_true, y_label)
        return score
    elif metric == "F1-score":
        score = metrics.f1_score(y_true, y_label)
        return score
    elif metric == "AUROC":
        score = metrics.roc_auc_score(y_true, y_pred)
        return score
    elif metric == "precision":
        score = metrics.precision_score(y_true, y_label)
        return score
    elif metric == "sensitivity":
        score = 1.0*tp/(tp+fn)
        return score
    elif metric == "specificity":
        score = 1.0*tn/(tn+fp)
        return score
    else:
        return score
    ### ========== TODO : END ========== ###


def cv_performance(clf, X, y, kf, metric="accuracy"):
    """
    Splits the data, X and y, into k-folds and runs k-fold cross-validation.
    Trains classifier on k-1 folds and tests on the remaining fold.
    Calculates the k-fold cross-validation performance metric for classifier
    by averaging the performance across folds.

    Parameters
    --------------------
        clf    -- classifier (instance of SVC)
        X      -- numpy array of shape (n,d), feature vectors
                    n = number of examples
                    d = number of features
        y      -- numpy array of shape (n,), binary labels {1,-1}
        kf     -- cross_validation.KFold or cross_validation.StratifiedKFold
        metric -- string, option used to select performance measure

    Returns
    --------------------
        score   -- float, average cross-validation performance across k folds
    """

    ### ========== TODO : START ========== ###
    # part 2b: compute average cross-validation performance
    score = 0;
    for train_index, validation_index in kf:
        X_train, X_validation = X[train_index], X[validation_index]
        y_train, y_validation = y[train_index], y[validation_index]
        clf.fit(X_train, y_train)
        y_pred = clf.decision_function(X_validation)
        score = score + performance(y_validation,y_pred,metric=metric)
    return score/5.0
    ### ========== TODO : END ========== ###


def select_param_linear(X, y, kf, metric="accuracy"):
    """
    Sweeps different settings for the hyperparameter of a linear-kernel SVM,
    calculating the k-fold CV performance for each setting, then selecting the
    hyperparameter that 'maximize' the average k-fold CV performance.

    Parameters
    --------------------
        X      -- numpy array of shape (n,d), feature vectors
                    n = number of examples
                    d = number of features
        y      -- numpy array of shape (n,), binary labels {1,-1}
        kf     -- cross_validation.KFold or cross_validation.StratifiedKFold
        metric -- string, option used to select performance measure

    Returns
    --------------------
        C -- float, optimal parameter value for linear-kernel SVM
    """
    print 'Linear SVM Hyperparameter Selection based on ' + str(metric) + ':'
    C_range = 10.0 ** np.arange(-3, 3)

    ### ========== TODO : START ========== ###
    # part 2c: select optimal hyperparameter using cross-validation
    metric_list = []
    for c in C_range:
        clf = SVC(kernel='linear', C = c)
        print cv_performance(clf,X,y,kf,metric=metric)
        metric_list.append(cv_performance(clf,X,y,kf,metric=metric))
    return C_range[metric_list.index(max(metric_list))]

    ### ========== TODO : END ========== ###


def select_param_rbf(X, y, kf, metric="accuracy"):
    """
    Sweeps different settings for the hyperparameters of an RBF-kernel SVM,
    calculating the k-fold CV performance for each setting, then selecting the
    hyperparameters that 'maximize' the average k-fold CV performance.
    
    Parameters
    --------------------
        X       -- numpy array of shape (n,d), feature vectors
                     n = number of examples
                     d = number of features
        y       -- numpy array of shape (n,), binary labels {1,-1}
        kf     -- cross_validation.KFold or cross_validation.StratifiedKFold
        metric  -- string, option used to select performance measure
    
    Returns
    --------------------
        gamma, C -- tuple of floats, optimal parameter values for an RBF-kernel SVM
    """
    
    print 'RBF SVM Hyperparameter Selection based on ' + str(metric) + ':'
    
    ### ========== TODO : START ========== ###
    # part 3b: create grid, then select optimal hyperparameters using cross-
    C_range = 10.0 ** np.arange(-3, 3)
    gamma_range = 10.0 ** np.arange(-3, 3)
    max_c = 0
    max_gamma = 0
    maxRate = 0
    for c in C_range:
        for gamma in gamma_range:
            clf = SVC(kernel = 'rbf', C=c, gamma = gamma)
            if cv_performance(clf, X, y, kf, metric=metric)>maxRate:
                maxRate = cv_performance(clf, X, y, kf, metric=metric)
                max_c = c
                max_gamma = gamma
    print maxRate
    return max_c, max_gamma
    ### ========== TODO : END ========== ###


def performance_test(clf, X, y, metric="accuracy"):
    """
    Estimates the performance of the classifier using the 95% CI.
    
    Parameters
    --------------------
        clf          -- classifier (instance of SVC)
                          [already fit to data]
        X            -- numpy array of shape (n,d), feature vectors of test set
                          n = number of examples
                          d = number of features
        y            -- numpy array of shape (n,), binary labels {1,-1} of test set
        metric       -- string, option used to select performance measure
    
    Returns
    --------------------
        score        -- float, classifier performance
    """

    ### ========== TODO : START ========== ###
    # part 4b: return performance on test data by first computing predictions and then calling performance

    score = 0        
    return score
    ### ========== TODO : END ========== ###


######################################################################
# main
######################################################################
 
def main() :
    np.random.seed(1234)
    
    # read the tweets and its labels   
    dictionary = extract_dictionary('../data/tweets.txt')
    X = extract_feature_vectors('../data/tweets.txt', dictionary)
    y = read_vector_file('../data/labels.txt')
    metric_list = ["accuracy", "f1_score", "auroc", "precision", "sensitivity", "specificity"]
    
    ### ========== TODO : START ========== ###
    # part 1c: split data into training (training + cross-validation) and testing set
    training_data = X[0:560, 0:]
    training_label = y[0:560]
    testing_data = X[560:, 0:]
    testing_label = y[560:]
    # part 2b: create stratified folds (5-fold CV)
    skf = StratifiedKFold(training_label, n_folds=5)
    # part 2d: for each metric, select optimal hyperparameter for linear-kernel SVM using CV
    #C_Accuracy=select_param_linear(training_data, training_label,skf)
    #print C_Accuracy
    #C_F1_score=select_param_linear(training_data, training_label, skf, metric="F1-score")
    #print C_F1_score
    #C_AUROC=select_param_linear(training_data, training_label, skf, metric="AUROC")
    #print C_AUROC
    #C_precision=select_param_linear(training_data, training_label, skf, metric="precision")
    #print C_precision
    #C_sensitivity=select_param_linear(training_data, training_label, skf, metric="sensitivity")
    #print C_sensitivity
    # part 3c: for each metric, select optimal hyperparameter for RBF-SVM using CV
    #C_Accuracy, gamma_Accuracy = select_param_rbf(training_data, training_label, skf)
    #print C_Accuracy
    #print gamma_Accuracy
    #C_F1_score, gamma_F1_score = select_param_rbf(training_data, training_label, skf, metric="F1-score")
    #print C_F1_score
    #print gamma_F1_score
    #C_AUROC, gamma_AUROC = select_param_rbf(training_data, training_label, skf, metric="AUROC")
    #print C_AUROC
    #print gamma_AUROC
    #C_precision, gamma_precision = select_param_rbf(training_data, training_label, skf, metric="precision")
    #print C_precision
    #print gamma_precision
    #C_sensitivity, gamma_sensitivity = select_param_rbf(training_data, training_label, skf, metric="sensitivity")
    #print C_sensitivity
    #print gamma_sensitivity
    #C_specificity, gamma_specificity = select_param_rbf(training_data, training_label, skf, metric="specificity")
    #print C_specificity
    #print gamma_specificity
    # part 4a: train linear- and RBF-kernel SVMs with selected hyperparameters
    clf_linear = SVC(kernel='linear', C=10)
    clf_rbf = SVC(kernel='rbf', C=100, gamma=0.01)
    clf_linear.fit(training_data, training_label)
    clf_rbf.fit(training_data, training_label)

    # part 4c: report performance on test data
    y_linear_pred = clf_linear.decision_function(testing_data)
    y_rbf_pred = clf_rbf.decision_function(testing_data)
    print "linear accuracy:"
    print(performance(testing_label, y_linear_pred))
    print "linear f1_score:"
    print(performance(testing_label, y_linear_pred, metric="F1-score"))
    print "linear AUROC:"
    print(performance(testing_label, y_linear_pred, metric="AUROC"))
    print "linear precision:"
    print(performance(testing_label, y_linear_pred, metric="precision"))
    print "linear sensitivity:"
    print(performance(testing_label, y_linear_pred, metric="sensitivity"))
    print "linear specificity:"
    print(performance(testing_label, y_linear_pred, metric="specificity"))

    print "rbf accuracy:"
    print(performance(testing_label, y_rbf_pred))
    print "rbf f1_score:"
    print(performance(testing_label, y_rbf_pred, metric="F1-score"))
    print "rbf AUROC:"
    print(performance(testing_label, y_rbf_pred, metric="AUROC"))
    print "rbf precision:"
    print(performance(testing_label, y_rbf_pred, metric="precision"))
    print "rbf sensitivity:"
    print(performance(testing_label, y_rbf_pred, metric="sensitivity"))
    print "rbf specificity:"
    print(performance(testing_label, y_rbf_pred, metric="specificity"))
    ### ========== TODO : END ========== ###
    
    
if __name__ == "__main__" :
    main()
