from utilities import process_data

f_acceleration_train_x = file("my_data_processed/acceleration_train_x.csv", "w")
f_gyroscope_train_x = file("my_data_processed/gyroscope_train_x.csv", "w")
f_acceleration_test_x = file("my_data_processed/acceleration_test_x.csv", "w")
f_gyroscope_test_x = file("my_data_processed/gyroscope_test_x.csv", "w")

f_acceleration_train_y = file("my_data_processed/acceleration_train_y.csv", "w")
f_gyroscope_train_y = file("my_data_processed/gyroscope_train_y.csv", "w")
f_acceleration_test_y = file("my_data_processed/acceleration_test_y.csv", "w")
f_gyroscope_test_y = file("my_data_processed/gyroscope_test_y.csv", "w")

f_acceleration_train_z = file("my_data_processed/acceleration_train_z.csv", "w")
f_gyroscope_train_z = file("my_data_processed/gyroscope_train_z.csv", "w")
f_acceleration_test_z = file("my_data_processed/acceleration_test_z.csv", "w")
f_gyroscope_test_z = file("my_data_processed/gyroscope_test_z.csv", "w")

f_activity_train = file("my_data_processed/activity_train.csv", "w")
f_activity_test = file("my_data_processed/activity_test.csv", "w")

acceleration_files = ["my_data/acceleration_sitting_hand.csv",
                      "my_data/acceleration_sitting_pocket.csv",
                      "my_data/acceleration_standing_hand.csv",
                      "my_data/acceleration_standing_pocket.csv",
                      "my_data/acceleration_up_down_stairs.csv",
                      "my_data/acceleration_walking_hand.csv",
                      "my_data/acceleration_walking_pocket.csv"]

gyroscope_files = ["my_data/gyroscope_sitting_hand.csv",
                   "my_data/gyroscope_sitting_pocket.csv",
                   "my_data/gyroscope_standing_hand.csv",
                   "my_data/gyroscope_standing_pocket.csv",
                   "my_data/gyroscope_up_down_stairs.csv",
                   "my_data/gyroscope_walking_hand.csv",
                   "my_data/gyroscope_walking_pocket.csv"]

for q in xrange(len(acceleration_files)):

    t, a, x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo = \
        process_data(acceleration_files[q], gyroscope_files[q])

    for i in xrange(len(t)):
        j = 0

        l = 0
        while len(t[i]) - j > 128:
            for k in xrange(j, j + 128):
                if k != j + 127:
                    if l % 3 == 2:
                        f_acceleration_test_x.write("%f," % x_acc[i][k])
                        f_acceleration_test_y.write("%f," % y_acc[i][k])
                        f_acceleration_test_z.write("%f," % z_acc[i][k])
                        
                        f_gyroscope_test_x.write("%f," % x_acc[i][k])
                        f_gyroscope_test_y.write("%f," % y_acc[i][k])
                        f_gyroscope_test_z.write("%f," % z_acc[i][k])
                        
                    else:
                        f_acceleration_train_x.write("%f," % x_acc[i][k])
                        f_acceleration_train_y.write("%f," % y_acc[i][k])
                        f_acceleration_train_z.write("%f," % z_acc[i][k])
                        
                        f_gyroscope_train_x.write("%f," % x_acc[i][k])
                        f_gyroscope_train_y.write("%f," % y_acc[i][k])
                        f_gyroscope_train_z.write("%f," % z_acc[i][k])
                else:
                    if l % 3 == 2:
                        f_acceleration_test_x.write("%f\n" % x_acc[i][k])
                        f_acceleration_test_y.write("%f\n" % y_acc[i][k])
                        f_acceleration_test_z.write("%f\n" % z_acc[i][k])
                        
                        f_gyroscope_test_x.write("%f\n" % x_acc[i][k])
                        f_gyroscope_test_y.write("%f\n" % y_acc[i][k])
                        f_gyroscope_test_z.write("%f\n" % z_acc[i][k])
                    else:
                        f_acceleration_train_x.write("%f\n" % x_acc[i][k])
                        f_acceleration_train_y.write("%f\n" % y_acc[i][k])
                        f_acceleration_train_z.write("%f\n" % z_acc[i][k])
                        
                        f_gyroscope_train_x.write("%f\n" % x_acc[i][k])
                        f_gyroscope_train_y.write("%f\n" % y_acc[i][k])
                        f_gyroscope_train_z.write("%f\n" % z_acc[i][k])

            if l % 3 == 2:
                f_activity_test.write("%d\n" % a[i])
            else:
                f_activity_train.write("%d\n" % a[i])

            l += 1

            j += 128