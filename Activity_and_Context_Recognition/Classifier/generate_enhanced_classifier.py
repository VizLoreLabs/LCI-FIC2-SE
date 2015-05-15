import numpy as np
from data_load import load_data_enhanced
from numpy import ndarray
from sklearn import svm, tree, naive_bayes
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier

target1, data1 = load_data_enhanced("my_data_processed/activity_train.csv",
                                    "my_data_processed/acceleration_train_x.csv",
                                    "my_data_processed/acceleration_train_y.csv",
                                    "my_data_processed/acceleration_train_z.csv",
                                    "my_data_processed/gyroscope_train_x.csv",
                                    "my_data_processed/gyroscope_train_y.csv",
                                    "my_data_processed/gyroscope_train_z.csv")

target2, data2 = load_data_enhanced("my_data_processed/activity_test.csv",
                                    "my_data_processed/acceleration_test_x.csv",
                                    "my_data_processed/acceleration_test_y.csv",
                                    "my_data_processed/acceleration_test_z.csv",
                                    "my_data_processed/gyroscope_test_x.csv",
                                    "my_data_processed/gyroscope_test_y.csv",
                                    "my_data_processed/gyroscope_test_z.csv")

data = np.append(data1, data2, 0)
target = np.append(target1, target2)

data = ndarray(shape=(len(data), 39), dtype=float, buffer=np.asanyarray(data))
target = ndarray(shape=(len(target),), dtype=int, buffer=np.asanyarray(target))


clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
clf.fit(data, target)
joblib.dump(clf, '../ActivityRecognition/activity_server/classifier/acc_gyo_ech/classifier_svc.pkl')

clf = tree.DecisionTreeClassifier()
clf.fit(data, target)
joblib.dump(clf, '../ActivityRecognition/activity_server/classifier/acc_gyo_ech/classifier_tree.pkl')