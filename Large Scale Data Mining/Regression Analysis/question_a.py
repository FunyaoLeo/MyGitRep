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

def linear_regression(features_scalar, labels_scalar, linear_model):
    linear_rmse_test_score=0
    linear_rmse_train_score=0
    linear_predict=[]
    linear_actual=[]
    kf = KFold(n_splits=10, random_state=0)
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
        linear_predict.append(labels_test_predict)
        linear_actual.append(labels_scalar_test)
    linear_predict = splitlist(linear_predict)
    linear_actual = splitlist(linear_actual)
    return linear_rmse_test_score/10, linear_rmse_train_score/10, linear_predict, linear_actual

 

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
    #plt.show()

    workflow_count = [[0 for i in range(105)] for i in range(5)]
    i = 0
    while i < len(week):
        workflow_count[workflow_list.index(workflow_id[i])][(week[i]-1)*7+day_of_week_list.index(day_of_week[i])]+=size_of_backup[i]
        i+=1
    for i in range(5):
        plt.plot([ j+1 for j in range(105)],workflow_count[i],label=workflow_list[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    #plt.show()

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
    linear_model = LinearRegression()
    features_scalar = np.array([week_scalar, day_of_week_scalar, backup_start_time_scalar, workflow_id_scalar, filename_scalar])
    features_scalar = features_scalar.transpose()

    labels_scalar = np.array([size_of_backup])
    labels_scalar = labels_scalar.transpose()
    linear_rmse_test_score, linear_rmse_train_score, linear_predict, linear_actual = linear_regression(features_scalar, labels_scalar, linear_model)
    plt.figure()
    plt.scatter(linear_actual,linear_predict, alpha=0.1)
    plt.ylim(min(linear_predict),max(linear_actual))
    plt.xlabel("Actual value")
    plt.ylabel("Fitted value")
    
    plt.figure()
    linear_residuals = list(map(lambda x: x[0]-x[1], zip(linear_actual, linear_predict))) 
    plt.scatter(linear_predict,linear_residuals, alpha=0.1)
    plt.xlim(min(linear_predict),max(linear_actual))
    plt.xlabel("Fitted value")
    plt.ylabel("Residual value")
    print(linear_rmse_test_score)
    
    #    standardize   ##
    #####################
    standard = StandardScaler()
    features_standard = standard.fit_transform(features_scalar)
    linear_model = LinearRegression()
    linear_rmse_test_score, linear_rmse_train_score, linear_predict, linear_actual = linear_regression(features_standard, labels_scalar, linear_model)
    plt.figure()
    plt.scatter(linear_actual,linear_predict, alpha=0.1)
    plt.ylim(min(linear_predict),max(linear_actual))
    plt.xlabel("Actual value")
    plt.ylabel("Fitted value")
    print(linear_rmse_test_score)

    #  three features  ##
    #####################
    
    Fval, pval = f_regression(features_scalar, labels_scalar)
    mval = mutual_info_regression(features_scalar, labels_scalar)
    print(Fval)
    print(mval)
    linear_model = LinearRegression()
    features_select = np.array([day_of_week_scalar, backup_start_time_scalar, workflow_id_scalar])
    features_select = features_select.transpose()

    linear_rmse_test_score, linear_rmse_train_score, linear_predict, linear_actual = linear_regression(features_select, labels_scalar, linear_model)
    print(linear_rmse_test_score)
    plt.figure()
    plt.scatter(linear_actual,linear_predict, alpha=0.1)
    plt.ylim(min(linear_predict),max(linear_actual))
    plt.xlabel("Actual value")
    plt.ylabel("Fitted value")
    plt.show()
    
    # 32 combinations of features ##
    ################################
    linear_rmse_test_result=[]
    linear_rmse_train_result=[]
    linear_model = LinearRegression()
    
    min_ridge_combination=0
    min_lasso_combination=0
    min_elastic_combination=0
    min_ridge_alpha=0
    min_lasso_alpha=0
    min_elastic_alpha=0
    min_ridge=1000
    min_lasso=1000
    min_elastic=1000
    
    for i in range(0,32):
        features = []
        if(i&1):
            features.append(np.array(week_scalar))
        else:
            features.append(np.array(week_one_hot))
        if(i>>1&1):
            features.append(np.array(day_of_week_scalar))
        else:
            features.append(np.array(day_of_week_one_hot))
        if(i>>2&1):
            features.append(np.array(backup_start_time_scalar))
        else:
            features.append(np.array(backup_start_time_one_hot))
        if(i>>3&1):
            features.append(np.array(workflow_id_scalar))
        else:
            features.append(np.array(workflow_id_one_hot))
        if(i>>4&1):
            features.append(np.array(filename_scalar))
        else:
            features.append(np.array(filename_one_hot))
        
        features = zip(*features)
        features_spilit=[]
        for j in range(len(features)):
            tmp = splitlist(features[j])
            features_spilit.append(tmp)
        #print(features)
        linear_rmse_test_score, linear_rmse_train_score, linear_predict, linear_actual = linear_regression(features_spilit, labels_scalar, linear_model)
        
        linear_rmse_test_result.append(linear_rmse_test_score)
        linear_rmse_train_result.append(linear_rmse_train_score)
        for al in np.arange(0.1,1,0.1):
            ridge_model = Ridge(alpha=al)
            ridge_rmse_test_score, ridge_rmse_train_score, ridge_predict, ridge_actual = linear_regression(features_spilit, labels_scalar, ridge_model)
            if(min_ridge>ridge_rmse_test_score):
                min_ridge_combination = i
                min_ridge_alpha = al
                min_ridge = ridge_rmse_test_score
        for al in np.arange(0.01,1,0.01):
            lasso_model = Lasso(alpha=al)
            lasso_rmse_test_score, lasso_rmse_train_score, linear_predict, linear_actual = linear_regression(features_spilit, labels_scalar, lasso_model)
            if(min_lasso>lasso_rmse_test_score):
                min_lasso_combination = i
                min_lasso_alpha = al
                min_lasso = lasso_rmse_test_score
        for al in np.arange(0.01,1,0.01):
            elastic_model = ElasticNet(alpha=al,l1_ratio=0.5)
            elastic_rmse_test_score, elastic_rmse_train_score, linear_predict, linear_actual = linear_regression(features_spilit, labels_scalar, elastic_model)
            if(min_elastic>elastic_rmse_test_score):
                min_elastic_combination = i
                min_elastic_alpha = al
                min_elastic = elastic_rmse_test_score
    plt.figure()
    plt.plot(linear_rmse_test_result,label="Testset")
    plt.plot(linear_rmse_train_result,label="Trainset")
    plt.legend(loc="best")
    print("The minimum test RMSE is combination: ")
    print(linear_rmse_test_result.index(min(linear_rmse_test_result)))
    print("The minimum train RMSE is combination: ")
    print(linear_rmse_train_result.index(min(linear_rmse_train_result)))
    print("The minimum ridge test RMSE is:%f and combination: %d with alpha is %f"%(min_ridge,min_ridge_combination,min_ridge_alpha))
    print("The minimum lasso test RMSE is:%f and combination: %d with alpha is %f"%(min_lasso,min_lasso_combination,min_lasso_alpha))
    print("The minimum elastic test RMSE is:%f and combination: %d with alpha is %f"%(min_elastic,min_elastic_combination,min_elastic_alpha))
        
    # Controlling ill-conditioning and over-fiting ##
    #################################################
    ridge_test_result=[]
    lasso_test_result=[]
    elastic_test_result=[]
    for al in np.arange(0.1,1,0.1):
        ridge_model = Ridge(alpha=al)
        ridge_rmse_test_score, ridge_rmse_train_score, linear_predict, linear_actual = linear_regression(features_scalar, labels_scalar, ridge_model)
        lasso_model = Lasso(alpha=al)
        lasso_rmse_test_score, lasso_rmse_train_score, linear_predict, linear_actual = linear_regression(features_scalar, labels_scalar, lasso_model)
        elastic_model = ElasticNet(alpha=0.5,l1_ratio=al)
        elastic_rmse_test_score, elastic_rmse_train_score, linear_predict, linear_actual = linear_regression(features_scalar, labels_scalar, elastic_model)
        ridge_test_result.append(ridge_rmse_test_score)
        lasso_test_result.append(lasso_rmse_test_score)
        elastic_test_result.append(elastic_rmse_test_score)
    print("The minimum ridge test RMSE happens when alpha is: ")
    print(0.1*(1+ridge_test_result.index(min(ridge_test_result))))
   
    print("The minimum lasso test RMSE happens when alpha is: ")
    print(0.1*(1+lasso_test_result.index(min(lasso_test_result))))
    
    print("The minimum elasticnet test RMSE happens when l1_ratio is: ")
    print(0.1*(1+elastic_test_result.index(min(elastic_test_result))))

        
    plt.show()


if __name__ == "__main__":
    main()