import numpy as np
from data_load import load_data
from numpy import ndarray
from sklearn import svm, tree, naive_bayes
from sklearn.externals import joblib

target1, data1 = load_data("my_data_processed/activity_train.csv",
                           "my_data_processed/acceleration_train_x.csv",
                           "my_data_processed/acceleration_train_y.csv",
                           "my_data_processed/acceleration_train_z.csv",
                           "my_data_processed/gyroscope_train_x.csv",
                           "my_data_processed/gyroscope_train_y.csv",
                           "my_data_processed/gyroscope_train_z.csv")

target2, data2 = load_data("my_data_processed/activity_test.csv",
                           "my_data_processed/acceleration_test_x.csv",
                           "my_data_processed/acceleration_test_y.csv",
                           "my_data_processed/acceleration_test_z.csv",
                           "my_data_processed/gyroscope_test_x.csv",
                           "my_data_processed/gyroscope_test_y.csv",
                           "my_data_processed/gyroscope_test_z.csv")

data = np.append(data1, data2, 0)
target = np.append(target1, target2)

data = ndarray(shape=(len(data), 21), dtype=float, buffer=np.asanyarray(data))
data = data[:, 0:12]
target = ndarray(shape=(len(target),), dtype=int, buffer=np.asanyarray(target))

clf = svm.SVC(probability=True)
clf.fit(data, target)
joblib.dump(clf, '../ActivityRecognition/activity_server/classifier/acc/classifier_svc.pkl')

clf = tree.DecisionTreeClassifier()
clf.fit(data, target)
joblib.dump(clf, '../ActivityRecognition/activity_server/classifier/acc/classifier_tree.pkl')