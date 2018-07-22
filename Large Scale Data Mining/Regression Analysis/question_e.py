import numpy as np
import matplotlib.pyplot as plt
from util import load_data_network
from sklearn.model_selection import KFold
import string
from sklearn import metrics
from sklearn.neighbors import KNeighborsRegressor

def knn(features, labels, n_neighbor):
    knn_rmse_train_set = []
    knn_rmse_test_set = []
    knn_predict = np.array([])
    knn_ground_truth = np.array([])
    kf = KFold(n_splits=10, random_state = 0, shuffle =True)
    for train_index, test_index in kf.split(features):
        features_train, labels_train = features[train_index], labels[train_index]
        features_test, labels_test = features[test_index], labels[test_index]
        k = KNeighborsRegressor(n_neighbors=n_neighbor)
        k.fit(features_train, labels_train)
        # trainset
        labels_train_predict = k.predict(features_train)
        knn_rmse_train_set.append(np.sqrt(metrics.mean_squared_error(labels_train, labels_train_predict)))
        # testset
        labels_test_predict = k.predict(features_test)
        labels_test_predict = labels_test_predict.transpose()
        labels_test_predict = labels_test_predict[0]
        labels_test = labels_test.transpose()
        labels_test = labels_test[0]
        knn_rmse_test_set.append(np.sqrt(metrics.mean_squared_error(labels_test, labels_test_predict)))

        knn_predict = np.concatenate((knn_predict, labels_test_predict))
        knn_ground_truth = np.concatenate((knn_ground_truth, labels_test))

    plt.scatter(range(len(knn_ground_truth)), knn_ground_truth, label='true values')
    plt.scatter(range(len(knn_predict)), knn_predict, label = 'fitted values')
    plt.legend(loc="lower right")
    plt.show()
    plt.scatter(range(len(knn_predict)), knn_predict, label='fitted values')
    plt.scatter(range(len(knn_ground_truth)), knn_predict - knn_ground_truth, label='residual values')
    plt.legend(loc="lower right")
    plt.show()

    return sum(knn_rmse_test_set) / 10.0, sum(knn_rmse_train_set) / 10.0

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


    # question e knn regression
    neighbors_range = range(1, 51)
    feature_train_error = []
    feature_test_error = []
    for neighbor in neighbors_range:
        rmse_test, rmse_train = knn(features=features_scalar, labels=labels_scalar, n_neighbor=neighbor)
        feature_test_error.append(rmse_test)
        feature_train_error.append(rmse_train)
    plt.plot(neighbors_range, feature_test_error, label="Test Error")
    plt.plot(neighbors_range, feature_train_error, label="Train Error")
    plt.legend(loc='lower right')
    plt.show()


    knn(features=features_scalar, labels=labels_scalar, n_neighbor=4)







if __name__ == "__main__":
    main()