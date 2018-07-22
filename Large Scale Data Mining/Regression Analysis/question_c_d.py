import numpy as np
import matplotlib.pyplot as plt
from util import load_data_network
from sklearn.model_selection import train_test_split
import string
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn import metrics
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import mutual_info_regression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import PolynomialFeatures

def neural_network(features, labels,hidden_layer, activity_function):
    clf = MLPRegressor(activation= activity_function ,solver='lbfgs', alpha=1e-5, hidden_layer_sizes = hidden_layer, random_state = 1)
    clf.fit(features, labels)
    return clf

def linear_regression(features_scalar, labels_scalar, model):
    linear_rmse_test_score=0
    linear_rmse_train_score=0
    kf = KFold(n_splits=10, random_state=0)
    if(model=="linear"):
        linear_model = LinearRegression()
    elif(model=="ridge"):
        linear_model = Ridge(alpha=0.5)
    elif(model=="lasso"):
        linear_model = Lasso(alpha=0.5)
    elif(model=="elasticnet"):
        linear_model = ElasticNet()
    for train_index, test_index in kf.split(features_scalar):

        features_scalar_train, labels_scalar_train = np.array(features_scalar)[train_index], np.array(labels_scalar)[train_index]
        features_scalar_test, labels_scalar_test = np.array(features_scalar)[test_index], np.array(labels_scalar)[test_index]
        linear_model.fit(features_scalar_train,labels_scalar_train)
        #testset
        labels_test_predict = linear_model.predict(features_scalar_test)
        linear_rmse_test = np.sqrt(metrics.mean_squared_error(labels_scalar_test, labels_test_predict))
        #trainset
        labels_train_predict = linear_model.predict(features_scalar_train)
        linear_rmse_train = np.sqrt(metrics.mean_squared_error(labels_scalar_train, labels_train_predict))
        
        linear_rmse_test_score += linear_rmse_test
        linear_rmse_train_score += linear_rmse_train
    return linear_rmse_test_score/10, linear_rmse_train_score/10

#online resource
def splitlist(list):  
    
    alist = []  
    a = 0  
  
    for sublist in list:
        try: 
            for i in sublist:  
                alist.append (i)  
        except TypeError: 
            alist.append(sublist)  
    for i in alist:  
        if type(i) == type([]):
            a =+ 1  
            break  
    if a==1:  
        return printlist(alist) 
    if a==0:  
        return alist  

def scalar_to_one_hot(data):
    max_number=max(data)
    result=[]
    for number in data:
        temp=[0 for i in range(max_number)]
        temp[number-1]=1
        result.append(temp)
    return np.array(result)

def main():
    dataset = load_data_network('network_backup_dataset.csv')
    week = dataset.week
    day_of_week = dataset.day_of_week
    backup_start_time = dataset.backup_start_time
    workflow_id = dataset.workflow_id
    filename = dataset.file_name
    size_of_backup = dataset.size_of_backup
    backup_time = dataset.backup_time

    #data_list=[week, day_of_week, backup_start_time, workflow_id,filename, size_of_backup, backup_time]
    workflow_list=['work_flow_0','work_flow_1','work_flow_2','work_flow_3','work_flow_4']
    week_list=[i+1 for i in range(15)]
    day_of_week_list=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    workflow_count= [[0 for i in range(20)]for i in range(5)]
    i=0
    while (week[i]-1)*7+day_of_week_list.index(day_of_week[i])+1 <=20:
        workflow_count[workflow_list.index(workflow_id[i])][(week[i]-1)*7+day_of_week_list.index(day_of_week[i])]+=size_of_backup[i]
        i+=1
    for i in range(5):
        plt.plot([ j+1 for j in range(20)], workflow_count[i],label=workflow_list[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

    workflow_count = [[0 for i in range(105)] for i in range(5)]
    i = 0
    while i < len(week):
        workflow_count[workflow_list.index(workflow_id[i])][(week[i]-1)*7+day_of_week_list.index(day_of_week[i])]+=size_of_backup[i]
        i+=1
    for i in range(5):
        plt.plot([ j+1 for j in range(105)],workflow_count[i],label=workflow_list[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

    # question a: Linear regression

    # part 1: scalarize the variable(all the scalar variables will have a subfix of "scalar)

    #####################
    #### dictionary #####
    #####################
    day_of_week_dict = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
    workflow_id_dict = {'work_flow_0': 1, 'work_flow_1': 2, 'work_flow_2': 3, 'work_flow_3': 4, 'work_flow_4': 5}



    # scalar variables ##
    #####################
    week_scalar = week
    day_of_week_scalar = []
    backup_start_time_scalar = backup_start_time
    workflow_id_scalar = []
    filename_scalar = []

    for day in day_of_week:
        day_of_week_scalar.append(day_of_week_dict[day])

    for ID in workflow_id:
        workflow_id_scalar.append(workflow_id_dict[ID])

    def filename_remove_string(filename):
        return int(string.replace(filename, "File_", ""))+1
    for name in filename:
        filename_scalar.append(filename_remove_string(name))

    
    week_one_hot = scalar_to_one_hot(week_scalar)
    day_of_week_one_hot = scalar_to_one_hot(day_of_week_scalar)
    backup_start_time_one_hot = scalar_to_one_hot(backup_start_time_scalar)
    workflow_id_one_hot = scalar_to_one_hot(workflow_id_scalar)
    filename_one_hot = scalar_to_one_hot(filename_scalar)
    
    #    directly use linear regression   ##
    ########################################
    features_scalar = np.array([week_scalar, day_of_week_scalar, backup_start_time_scalar, workflow_id_scalar, filename_scalar])
    features_scalar = features_scalar.transpose()

    labels_scalar = np.array([size_of_backup])
    labels_scalar = labels_scalar.transpose()
    linear_rmse_test_score, linear_rmse_train_score = linear_regression(features_scalar, labels_scalar, "linear")


    #question c
    features_one_hot=[week_one_hot,day_of_week_one_hot,backup_start_time_one_hot,workflow_id_one_hot,filename_one_hot]
    features_one_hot = zip(*features_one_hot)
    features = []
    for j in range(len(features_one_hot)):
        tmp = splitlist(features_one_hot[j])
        features.append(tmp)

    activity_function_list=['relu','logistic','tanh']
    kf = KFold(n_splits=10, random_state=0)
    rmse_relu=[]
    rmse_logistic=[]
    rmse_tanh=[]
    label=np.array(size_of_backup)
    label=label.astype('float')
    """for activity_function in activity_function_list:
        for i in range(10,201,10):
            rmse=0
            for train_index, test_index in kf.split(features):
                features_train, labels_train = np.asarray(features)[train_index], label[train_index]
                features_test, labels_test = np.asarray(features)[test_index], label[test_index]
                clf = neural_network(features_train, labels_train, i, activity_function)
                labels_predict=clf.predict(features_test)
                rmse_test = np.sqrt(metrics.mean_squared_error(labels_test, labels_predict))
                rmse=rmse+rmse_test
            rmse=rmse/10
            if(activity_function=='relu'):
                rmse_relu.append(rmse)
            if (activity_function == 'logistic'):
                rmse_logistic.append(rmse)
            if (activity_function == 'tanh'):
                rmse_tanh.append(rmse)
            print('hidden units= %i  activity function= %s' %(i, activity_function))
            print rmse
    plt.plot([i for i in range(10, 201, 10)], rmse_relu, color='r')
    plt.show()
    plt.plot([i for i in range(10, 201, 10)], rmse_relu, color='r')
    plt.plot([i for i in range(10, 201, 10)], rmse_logistic, color='g')
    plt.plot([i for i in range(10, 201,10)],rmse_tanh,color='b')

    print 'begin'
    fit_value = []
    true_value = []
    for train_index, test_index in kf.split(features):
        features_train, labels_train = np.asarray(features)[train_index], label[train_index]
        features_test, labels_test = np.asarray(features)[test_index], label[test_index]
        clf = neural_network(features_train, labels_train, 20, 'relu')
        labels_predict = clf.predict(features_test)
        labels_test = list(labels_test)
        labels_predict = list(labels_predict)
        fit_value.extend(labels_predict)
        true_value.extend(labels_test)

    plt.scatter(true_value, fit_value)
    plt.show()
    fit_value = np.array(fit_value)
    true_value = np.array(true_value)
    residual = true_value - fit_value
    true_value = list(true_value)
    residual = list(residual)
    plt.scatter(fit_value, residual)
    plt.show()
    plt.scatter([i+1 for i in range(len(features))],fit_value,color='b',label='fit_value')
    plt.scatter([i+1 for i in range(len(features))],true_value,color='g',label='true_value')
    plt.legend(loc='upper right')
    plt.show()
    plt.scatter([i+1 for i in range(len(features))],fit_value,color='b',label='fit_value')
    plt.scatter([i+1 for i in range(len(features))],residual,color='g',label='redidual')
    plt.legend(loc='upper right')
    plt.show()"""






    #question d
    features_scalar = np.array([week_scalar, day_of_week_scalar, backup_start_time_scalar, workflow_id_scalar, filename_scalar])
    features_scalar = features_scalar.transpose()
    label = np.array(size_of_backup)
    workflow_list=[[] for i in range(5)]
    label_list=[[]for i in range(5)]
    for i in range(len(features_scalar)):
        workflow_list[features_scalar[i][3]-1].append(features_scalar[i])
        label_list[features_scalar[i][3]-1].append(label[i])


    """kf = KFold(n_splits=10, random_state=0)
    rmse=[0 for i in range(5)]
    for i in range(5):
        for train_index, test_index in kf.split(workflow_list[i]):
            train_feature, train_label=np.array(workflow_list[i])[train_index],np.array(label_list[i])[train_index]
            test_feature, test_label= np.array(workflow_list[i])[test_index],np.array(label_list[i])[test_index]
            lr=LinearRegression()
            lr.fit(train_feature,train_label)
            label_predict=lr.predict(test_feature)
            linear_rmse_test = np.sqrt(metrics.mean_squared_error(test_label, label_predict))
            rmse[i]=rmse[i]+linear_rmse_test
        rmse[i]=rmse[i]/10
    print rmse"""

    rmse=[[0 for i in range(2,11)] for i in range(5)]
    rmse_train=[[0 for i in range(2,11)] for i in range(5)]
    fit_value=[]
    true_value=[]
    for i in range(5):
        for j in range(2,11):
            poly=PolynomialFeatures(degree=j)
            workflow_temp=poly.fit_transform(workflow_list[i])
            for train_index, test_index in kf.split(workflow_temp):
                train_feature, train_label=np.array(workflow_temp)[train_index],np.array(label_list[i])[train_index]
                test_feature, test_label= np.array(workflow_temp)[test_index],np.array(label_list[i])[test_index]
                lr=LinearRegression()
                lr.fit(train_feature,train_label)
                label_predict=lr.predict(test_feature)
                label_train_predict=lr.predict(train_feature)
                linear_rmse_train=np.sqrt(metrics.mean_squared_error(train_label, label_train_predict))
                linear_rmse_test = np.sqrt(metrics.mean_squared_error(test_label, label_predict))
                rmse_train[i][j-2]=rmse_train[i][j-2]+linear_rmse_train
                rmse[i][j-2]=rmse[i][j-2]+linear_rmse_test
                test_label=list(test_label)
                label_predict=list(label_predict)
                fit_value.extend(label_predict)
                true_value.extend(test_label)
            rmse_train[i][j-2]=rmse_train[i][j-2]/10
            rmse[i][j-2]=rmse[i][j-2]/10
            print('i=%i , j= %i'%(i,j))
            print('rmse_train: %f' %rmse_train[i][j-2] )
            print('rmse: %f' % rmse[i][j-2])

    print rmse
    print rmse_train
    workflow_list_sign = ['work_flow_0', 'work_flow_1', 'work_flow_2', 'work_flow_3', 'work_flow_4']
    for i in range(5):
        plt.plot([j for j in range(2,11)], rmse_train[i],label=workflow_list_sign[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    for i in range(5):
        plt.plot([j for j in range(2,11)], rmse[i],label=workflow_list_sign[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    plt.scatter(true_value,fit_value)
    plt.show()
    fit_value=np.array(fit_value)
    true_value=np.array(true_value)
    residual=true_value-fit_value
    true_value=list(true_value)
    residual=list(residual)
    plt.scatter(fit_value, residual)
    plt.show()

    plt.scatter([i + 1 for i in range(len(fit_value))], fit_value, color='b', label='fit_value')
    plt.scatter([i + 1 for i in range(len(true_value))], true_value, color='g', label='true_value')
    plt.legend(loc='upper right')
    plt.show()
    plt.scatter([i + 1 for i in range(len(fit_value))], fit_value, color='b', label='fit_value')
    plt.scatter([i + 1 for i in range(len(true_value))], residual, color='g', label='redidual')
    plt.legend(loc='upper right')
    plt.show()

if __name__ == "__main__":
    main()