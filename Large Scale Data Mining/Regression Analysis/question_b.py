import os
import numpy as np
import matplotlib.pyplot as plt
from util import load_data_network
from sklearn.model_selection import KFold
import string
from sklearn import metrics
from sklearn.tree import export_graphviz
from sklearn.ensemble import RandomForestRegressor

def random_forest(features, labels, num_trees, num_features, max_depth):
    rf_rmse_train_set = []
    rf_rmse_test_set = []
    rf_feature_importance_set = []
    rf_predict = np.array([])
    rf_ground_truth = np.array([])
    kf = KFold(n_splits=10, shuffle = True)

    for train_index, test_index in kf.split(features):
        features_train, labels_train = features[train_index], labels[train_index]
        features_test, labels_test = features[test_index], labels[test_index]
        rf = RandomForestRegressor(n_estimators=num_trees, max_depth=max_depth, max_features=num_features, oob_score=True)
        rf.fit(features_train, labels_train)
        #trainset
        labels_train_predict = rf.predict(features_train)
        rf_rmse_train_set.append(np.sqrt(metrics.mean_squared_error(labels_train, labels_train_predict)))
        #testset
        labels_test_predict = rf.predict(features_test)
        labels_test = labels_test.transpose()
        labels_test = labels_test[0]
        rf_predict = np.concatenate((rf_predict, labels_test_predict))
        rf_ground_truth = np.concatenate((rf_ground_truth, labels_test))
        rf_rmse_test_set.append(np.sqrt(metrics.mean_squared_error(labels_test, labels_test_predict)))
        rf_feature_importance_set.append(rf.feature_importances_)
    plt.scatter(range(len(rf_ground_truth)), rf_ground_truth, label='true values')
    plt.scatter(range(len(rf_predict)), rf_predict, label='fitted values')
    plt.legend(loc="lower right")
    plt.show()
    plt.scatter(range(len(rf_predict)), rf_predict, label='fitted values')
    plt.scatter(range(len(rf_ground_truth)), rf_predict - rf_ground_truth, label='residual values')
    plt.legend(loc="lower right")
    plt.show()
    feature_names = ["week", "day_of_week", "backup_start_time", "workflow_id", "filename"]
    export_graphviz(rf.estimators_[17], feature_names=feature_names)
    os.system('dot -Tpng tree.dot -o tree.png')
    print "feature importances"
    print sum(rf_feature_importance_set)/10.0
    return sum(rf_rmse_test_set)/10.0, sum(rf_rmse_train_set)/10.0, 1-rf.oob_score_

def main():
    dataset = load_data_network('network_backup_dataset.csv')
    week = dataset.week
    day_of_week = dataset.day_of_week
    backup_start_time = dataset.backup_start_time
    workflow_id = dataset.workflow_id
    filename = dataset.file_name
    size_of_backup = dataset.size_of_backup
    backup_time = dataset.backup_time

    #####################
    #### dictionary #####
    #####################
    day_of_week_dict = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6,
                        "Sunday": 7}
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
        return int(string.replace(filename, "File_", "")) + 1

    for name in filename:
        filename_scalar.append(filename_remove_string(name))

    ##   directly use linear regression   ##
    ########################################
    features_scalar = np.array(
        [week_scalar, day_of_week_scalar, backup_start_time_scalar, workflow_id_scalar, filename_scalar])
    features_scalar = features_scalar.transpose()
    labels_scalar = np.array([size_of_backup])
    labels_scalar = labels_scalar.transpose()

    # Question b: Random Forest Method

    # subquestion i:
    print 'Test RMSE, Train RMSE, OOB error: '
    print random_forest(features=features_scalar, labels=labels_scalar, num_trees=20, num_features=5, max_depth=4)
    
    # subquestion ii:
    ## first is oob error
    tree_range = range(1, 201)
    feature_range = range(1, 6)
    for num_feature in feature_range:
        feature_oob_error = []
        for num_tree in tree_range:
            rmse_test, rmse_train, oob_error = random_forest(features=features_scalar, labels=labels_scalar,
                                                             num_trees=num_tree, num_features=num_feature, max_depth=4)
            feature_oob_error.append(oob_error)
        plt.plot(tree_range, feature_oob_error, label=str(num_feature))
    plt.title("OOB error")
    plt.legend(loc='lower right')
    plt.show()

    ## second is test rmse error
    tree_range = range(1, 201)
    feature_range = range(1, 6)
    for num_feature in feature_range:
        feature_test_rmse_error = []
        for num_tree in tree_range:
            rmse_test, rmse_train, oob_error = random_forest(features=features_scalar, labels=labels_scalar,
                                                             num_trees=num_tree, num_features=num_feature, max_depth=4)
            feature_test_rmse_error.append(rmse_test)
        plt.plot(tree_range, feature_test_rmse_error, label=str(num_feature))
    plt.title("Test RMSE error")
    plt.legend(loc='lower right')
    plt.show()
    
    # subquestion iii:
    depth_range = range(1, 21)
    depth_oob_error = []
    depth_test_error = []
    for depth in depth_range:
        rmse_test, rmse_train, oob_error = random_forest(features=features_scalar, labels=labels_scalar,
                                                         num_trees=25, num_features=4, max_depth=depth)
        depth_oob_error.append(oob_error)
        depth_test_error.append(rmse_test)
    plt.plot(depth_range, depth_oob_error)
    plt.title("OOB Error")
    plt.show()

    plt.plot(depth_range, depth_test_error)
    plt.title("Test RMSE Error")
    plt.show()

    # subquestion iv:
    random_forest(features=features_scalar, labels=labels_scalar, num_trees=25, num_features=4, max_depth=4)

if __name__ == "__main__":
    main()