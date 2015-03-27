import numpy as np
from data_load import load_data_enhanced
from numpy import ndarray
from sklearn import svm, tree, naive_bayes

target, data = load_data_enhanced("my_data_processed/activity_train.csv",
                                  "my_data_processed/acceleration_train_x.csv",
                                  "my_data_processed/acceleration_train_y.csv",
                                  "my_data_processed/acceleration_train_z.csv",
                                  "my_data_processed/gyroscope_train_x.csv",
                                  "my_data_processed/gyroscope_train_y.csv",
                                  "my_data_processed/gyroscope_train_z.csv")

data = ndarray(shape=(len(data), 39), dtype=float, buffer=np.asanyarray(data))
target = ndarray(shape=(len(target),), dtype=int, buffer=np.asanyarray(target))

clf = svm.SVC()
clf.fit(data, target)

target, data = load_data_enhanced("my_data_processed/activity_test.csv",
                                  "my_data_processed/acceleration_test_x.csv",
                                  "my_data_processed/acceleration_test_y.csv",
                                  "my_data_processed/acceleration_test_z.csv",
                                  "my_data_processed/gyroscope_test_x.csv",
                                  "my_data_processed/gyroscope_test_y.csv",
                                  "my_data_processed/gyroscope_test_z.csv")

data = ndarray(shape=(len(data), 39), dtype=float, buffer=np.asanyarray(data))
target = ndarray(shape=(len(target),), dtype=int, buffer=np.asanyarray(target))

y_predicted = clf.predict(data)
print("Number of mislabeled points out of a total %d points : %d" % (data.shape[0], (target != y_predicted).sum()))