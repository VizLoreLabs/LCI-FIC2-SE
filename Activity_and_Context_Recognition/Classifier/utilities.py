import numpy as np
from scipy.signal import butter, lfilter, medfilt
from scipy.interpolate import interp1d

activity_table = {"Sitting Hand\n": 1,
                  "Sitting Pocket\n": 2,
                  "Walking Hand\n": 3,
                  "Walking Pocket\n": 4,
                  "Standing Hand\n": 5,
                  "Standing Pocket\n": 6,
                  "Upstairs\n": 7,
                  "Downstairs\n": 8}


def load_data(file_name):
    f = open(file_name, 'r')

    a = []
    x = []
    y = []
    z = []
    t = []

    for line in f:
        columns = line.split(',')

        t.append(long(columns[0]))
        x.append(float(columns[1]))
        y.append(float(columns[2]))
        z.append(float(columns[3]))
        a.append(activity_table.get(columns[4]))

    return x, y, z, t, a


def get_chunks(x, y, z, a, t):

    x_chunks = []
    y_chunks = []
    z_chunks = []
    t_chunks = []
    a_chunks = []

    x_chunk = []
    y_chunk = []
    z_chunk = []
    t_chunk = []

    prev_t = t[0]
    a_chunks.append(a[0])

    for i in xrange(len(t)):

        if t[i] - prev_t > 80000000:
            x_chunks.append(x_chunk)
            y_chunks.append(y_chunk)
            z_chunks.append(z_chunk)
            t_chunks.append(t_chunk)

            x_chunk = []
            y_chunk = []
            z_chunk = []
            t_chunk = []
            a_chunks.append(a[i])

        x_chunk.append(x[i])
        y_chunk.append(y[i])
        z_chunk.append(z[i])
        t_chunk.append(t[i])
        prev_t = t[i]

    if t_chunk:
        x_chunks.append(x_chunk)
        y_chunks.append(y_chunk)
        z_chunks.append(z_chunk)
        t_chunks.append(t_chunk)

    return x_chunks, y_chunks, z_chunks, a_chunks, t_chunks


def resample_data(x_acc, y_acc, z_acc, t_acc, x_gyo, y_gyo, z_gyo, t_gyo):

    t_begin = max(t_acc[0], t_gyo[0])
    t_end = min(t_acc[-1], t_gyo[-1])

    f_x_acc = interp1d(t_acc, x_acc)
    f_y_acc = interp1d(t_acc, y_acc)
    f_z_acc = interp1d(t_acc, z_acc)
    
    f_x_gyo = interp1d(t_gyo, x_gyo)
    f_y_gyo = interp1d(t_gyo, y_gyo)
    f_z_gyo = interp1d(t_gyo, z_gyo)

    size = (t_end - t_begin)//20000000

    t = np.linspace(t_begin, t_begin + size * 20000000, size)

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


def process_data(filename_acc, filename_gyo):
    x_acc, y_acc, z_acc, t_acc, a_acc = load_data(filename_acc)
    x_gyo, y_gyo, z_gyo, t_gyo, a_gyo = load_data(filename_gyo)

    x_acc, y_acc, z_acc, a_acc, t_acc = get_chunks(x_acc, y_acc, z_acc, a_acc, t_acc)
    x_gyo, y_gyo, z_gyo, a_gyo, t_gyo = get_chunks(x_gyo, y_gyo, z_gyo, a_gyo, t_gyo)

    a = []

    for i in xrange(len(t_gyo)):
        if a_gyo[i] == a_acc[i]:
            t_acc[i], x_acc[i], y_acc[i], z_acc[i], x_gyo[i], y_gyo[i], z_gyo[i] = \
                resample_data(x_acc[i], y_acc[i], z_acc[i], t_acc[i], x_gyo[i], y_gyo[i], z_gyo[i], t_gyo[i])

            x_acc[i], y_acc[i], z_acc[i] = filter_acceleration(x_acc[i], y_acc[i], z_acc[i])
            x_gyo[i], y_gyo[i], z_gyo[i] = filter_gyroscope(x_gyo[i], y_gyo[i], z_gyo[i])
            a.append(a_acc[i])

    return t_acc, a, x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo