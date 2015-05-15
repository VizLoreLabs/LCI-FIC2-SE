import numpy as np
from activity_server.models import DataRecord, ActivityEntry, LocationEntry, WifiEntry
from datetime import datetime
from scipy.signal import butter, lfilter, medfilt
from scipy.interpolate import interp1d
from activity_server.utilities.statistics import get_features, get_features_acceleration
from activity_server.utilities.statistics import get_enhanced_features, get_enhanced_features_acceleration
from sklearn.externals import joblib

svc_acc_gyo = joblib.load('./activity_server/classifier/acc_gyo/classifier_svc.pkl')
svc_acc = joblib.load('./activity_server/classifier/acc/classifier_svc.pkl')
tree_acc_gyo = joblib.load('./activity_server/classifier/acc_gyo/classifier_tree.pkl')
tree_acc = joblib.load('./activity_server/classifier/acc/classifier_tree.pkl')

svc_acc_gyo_ech = joblib.load('./activity_server/classifier/acc_gyo_ech/classifier_svc.pkl')
svc_acc_ech = joblib.load('./activity_server/classifier/acc_ech/classifier_svc.pkl')
tree_acc_gyo_ech = joblib.load('./activity_server/classifier/acc_gyo_ech/classifier_tree.pkl')
tree_acc_ech = joblib.load('./activity_server/classifier/acc_ech/classifier_tree.pkl')


def store_data_record(json_object):
    if 'uuid' in json_object.keys() and \
       'acceleration' in json_object.keys() and \
       'gyroscope' in json_object.keys() and \
       'location' in json_object.keys() and \
       'wifi' in json_object.keys():

        if json_object.get('gyroscope'):
            t, x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo = process_data(json_object.get('acceleration'),
                                                                       json_object.get('gyroscope'))

            data = get_features(x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo)
            svm = svc_acc_gyo.predict_proba(data)[0]
            dt = tree_acc_gyo.predict_proba(data)[0]

            data = get_enhanced_features(x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo)
            svm_ech = svc_acc_gyo_ech.predict_proba(data)[0]
            dt_ech = tree_acc_gyo_ech.predict_proba(data)[0]
        else:
            t, x_acc, y_acc, z_acc = process_acceleration_data(json_object.get('acceleration'))

            data = get_features_acceleration(x_acc, y_acc, z_acc)
            svm = svc_acc.predict_proba(data)[0]
            dt = tree_acc.predict_proba(data)[0]

            data = get_enhanced_features_acceleration(x_acc, y_acc, z_acc)
            svm_ech = svc_acc_ech.predict_proba(data)[0]
            dt_ech = tree_acc_ech.predict_proba(data)[0]

        activity_entry = ActivityEntry(svm=svm.tolist(),
                                       svm_ech=svm_ech.tolist(),
                                       dt=dt.tolist(),
                                       dt_ech=dt_ech.tolist())

        locations_entry = process_locations(json_object.get('location'))
        wifi_entry = process_wifi(json_object.get('wifi'))

        data_record = DataRecord(user_id=json_object.get('uuid'),
                                 date_time=datetime.utcnow(),
                                 activity=activity_entry,
                                 wifi=wifi_entry,
                                 location=locations_entry)
        data_record.save()
    else:
        raise Exception("Invalid json format")


def process_data(acceleration_data, gyroscope_data):
    x_acc = np.zeros(len(acceleration_data), dtype=float)
    y_acc = np.zeros(len(acceleration_data), dtype=float)
    z_acc = np.zeros(len(acceleration_data), dtype=float)
    t_acc = np.zeros(len(acceleration_data), dtype=long)

    x_gyo = np.zeros(len(gyroscope_data), dtype=float)
    y_gyo = np.zeros(len(gyroscope_data), dtype=float)
    z_gyo = np.zeros(len(gyroscope_data), dtype=float)
    t_gyo = np.zeros(len(gyroscope_data), dtype=float)

    for i in xrange(len(acceleration_data)):
        x_acc[i] = acceleration_data[i].get('x')
        y_acc[i] = acceleration_data[i].get('y')
        z_acc[i] = acceleration_data[i].get('z')
        t_acc[i] = acceleration_data[i].get('timestamp')

    for i in xrange(len(gyroscope_data)):
        x_gyo[i] = gyroscope_data[i].get('x')
        y_gyo[i] = gyroscope_data[i].get('y')
        z_gyo[i] = gyroscope_data[i].get('z')
        t_gyo[i] = gyroscope_data[i].get('timestamp')

    t, x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo = resample_data(x_acc, y_acc, z_acc, t_acc, x_gyo, y_gyo, z_gyo, t_gyo)
    x_acc, y_acc, z_acc = filter_acceleration(x_acc, y_acc, z_acc)
    x_gyo, y_gyo, z_gyo = filter_gyroscope(x_gyo, y_gyo, z_gyo)

    return t, x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo


def process_acceleration_data(acceleration_data):
    x = np.zeros(len(acceleration_data), dtype=float)
    y = np.zeros(len(acceleration_data), dtype=float)
    z = np.zeros(len(acceleration_data), dtype=float)
    t = np.zeros(len(acceleration_data), dtype=long)

    for i in xrange(len(acceleration_data)):
        x[i] = acceleration_data[i].get('x')
        y[i] = acceleration_data[i].get('y')
        z[i] = acceleration_data[i].get('z')
        t[i] = acceleration_data[i].get('timestamp')

    t, x, y, z = resample_acceleration_data(x, y, z, t)
    x, y, z = filter_acceleration(x, y, z)

    return t, x, y, z


def resample_acceleration_data(x, y, z, t):

    t_begin = t[0]
    t_end = t[-1]

    f_x_acc = interp1d(t, x)
    f_y_acc = interp1d(t, y)
    f_z_acc = interp1d(t, z)

    size = (t_end - t_begin)//20

    t = np.linspace(t_begin, t_begin + size * 20, size)

    x = f_x_acc(t)
    y = f_y_acc(t)
    z = f_z_acc(t)

    return t, x, y, z


def resample_data(x_acc, y_acc, z_acc, t_acc, x_gyo, y_gyo, z_gyo, t_gyo):
    t_begin = max(t_acc[0], t_gyo[0])
    t_end = min(t_acc[-1], t_gyo[-1])

    f_x_acc = interp1d(t_acc, x_acc)
    f_y_acc = interp1d(t_acc, y_acc)
    f_z_acc = interp1d(t_acc, z_acc)

    f_x_gyo = interp1d(t_gyo, x_gyo)
    f_y_gyo = interp1d(t_gyo, y_gyo)
    f_z_gyo = interp1d(t_gyo, z_gyo)

    size = (t_end - t_begin)//20

    t = np.linspace(t_begin, t_begin + size * 20, size)

    x_acc = f_x_acc(t)
    y_acc = f_y_acc(t)
    z_acc = f_z_acc(t)

    x_gyo = f_x_gyo(t)
    y_gyo = f_y_gyo(t)
    z_gyo = f_z_gyo(t)

    return t, x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo


def butter_bandpass(low_cut, high_cut, fs, order=5):
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(x, low_cut, high_cut, fs, order=5):
    b, a = butter_bandpass(low_cut, high_cut, fs, order=order)
    y = lfilter(b, a, x)
    return y


def filter_acceleration(x, y, z):
    x = medfilt(np.array(x))
    y = medfilt(np.array(y))
    z = medfilt(np.array(z))

    x = butter_bandpass_filter(x, 0, 20, 50, order=3)
    y = butter_bandpass_filter(y, 0, 20, 50, order=3)
    z = butter_bandpass_filter(z, 0, 20, 50, order=3)

    return x, y, z


def filter_gyroscope(x, y, z):
    x = medfilt(np.array(x))
    y = medfilt(np.array(y))
    z = medfilt(np.array(z))

    x = butter_bandpass_filter(x, 0.3, 20, 50, order=3)
    y = butter_bandpass_filter(y, 0.3, 20, 50, order=3)
    z = butter_bandpass_filter(z, 0.3, 20, 50, order=3)

    return x, y, z


def process_locations(locations):
    result = []
    for location in locations:
        result.append(LocationEntry(time_stamp=location.get('timestamp'),
                                    lat=location.get('coords').get('lat'),
                                    lon=location.get('coords').get('lot')))
    return result


def process_wifi(wifi_data):
    result = []
    for wifi in wifi_data:
        result.append(WifiEntry(time_stamp=wifi.get('timestamp'),
                                ssids=wifi.get('ssids')))
    return result