from numpy import ndarray, array
from math import sqrt


def get_mean(x_array):
    return sum(x_array) / len(x_array)


def get_standard_deviation(x_array, mean):
    s = 0
    for i in xrange(len(x_array)):
        s += (x_array[i] - mean)**2
    return sqrt(s / len(x_array))


def get_energy(x_array):
    s = 0
    for i in xrange(len(x_array)):
        s += x_array[i]**2
    return s / len(x_array)


def get_correlation(x_array, y_array, x_mean, y_mean, x_sd, y_sd):
    s = 0
    for i in range(len(x_array)):
        s += (x_array[i] - x_mean)*(y_array[i] - y_mean)
    return s / (len(x_array)*x_sd*y_sd)


def get_min(x_array):
    return min(x_array)


def get_max(x_array):
    return max(x_array)


def get_mad(x_array, x_mean):
    x_m_array = []
    for value in x_array:
        x_m_array.append(abs(value - x_mean))
    return get_mean(x_m_array)


def load_data(results_filename,
              acc_x_filename, acc_y_filename, acc_z_filename,
              gyo_x_filename, gyo_y_filename, gyo_z_filename):

    subject = open(results_filename, 'r')
    subject_data = []

    for line in subject:
        subject_data.append(int(line))

    target = ndarray(shape=(len(subject_data),), dtype=int, buffer=array(subject_data))

    x_data = []
    x_mean = []
    x_energy = []
    x_st_deviation = []

    x_file = open(acc_x_filename, 'r')

    for line in x_file:
        x_values = line.split(',')
        temp = []
        for value in x_values:
            temp.append(float(value))
        mean = get_mean(temp)

        x_data.append(temp)
        x_mean.append(mean)
        x_energy.append(get_energy(temp))
        x_st_deviation.append(get_standard_deviation(temp, mean))

    y_data = []
    y_mean = []
    y_energy = []
    y_st_deviation = []

    y_file = open(acc_y_filename, 'r')

    for line in y_file:
        y_values = line.split(',')
        temp = []
        for value in y_values:
            temp.append(float(value))
        mean = get_mean(temp)

        y_data.append(temp)
        y_mean.append(mean)
        y_energy.append(get_energy(temp))
        y_st_deviation.append(get_standard_deviation(temp, mean))

    z_data = []
    z_mean = []
    z_energy = []
    z_st_deviation = []

    z_file = open(acc_z_filename, 'r')

    for line in z_file:
        z_values = line.split(',')
        temp = []
        for value in z_values:
            temp.append(float(value))
        mean = get_mean(temp)

        z_data.append(temp)
        z_mean.append(mean)
        z_energy.append(get_energy(temp))
        z_st_deviation.append(get_standard_deviation(temp, mean))

    xy_cor = []
    xz_cor = []
    zy_cor = []

    for i in xrange(len(x_data)):

        cor_xy = get_correlation(x_data[i], y_data[i], x_mean[i], y_mean[i], x_st_deviation[i], y_st_deviation[i])
        cor_xz = get_correlation(x_data[i], z_data[i], x_mean[i], z_mean[i], x_st_deviation[i], z_st_deviation[i])
        cor_zy = get_correlation(z_data[i], y_data[i], z_mean[i], y_mean[i], z_st_deviation[i], y_st_deviation[i])

        xy_cor.append(cor_xy)
        xz_cor.append(cor_xz)
        zy_cor.append(cor_zy)

    x_data_gyo = []
    x_mean_gyo = []
    x_st_deviation_gyo = []

    x_file = open(gyo_x_filename, 'r')

    for line in x_file:
        x_values = line.split(',')
        temp = []
        for value in x_values:
            temp.append(float(value))
        mean = get_mean(temp)

        x_data_gyo.append(temp)
        x_mean_gyo.append(mean)
        x_st_deviation_gyo.append(get_standard_deviation(temp, mean))

    y_data_gyo = []
    y_mean_gyo = []
    y_st_deviation_gyo = []

    y_file = open(gyo_y_filename, 'r')

    for line in y_file:
        y_values = line.split(',')
        temp = []
        for value in y_values:
            temp.append(float(value))
        mean = get_mean(temp)

        y_data_gyo.append(temp)
        y_mean_gyo.append(mean)
        y_st_deviation_gyo.append(get_standard_deviation(temp, mean))

    z_data_gyo = []
    z_mean_gyo = []
    z_st_deviation_gyo = []

    z_file = open(gyo_z_filename, 'r')

    for line in z_file:
        z_values = line.split(',')
        temp = []
        for value in z_values:
            temp.append(float(value))
        mean = get_mean(temp)

        z_data_gyo.append(temp)
        z_mean_gyo.append(mean)
        z_st_deviation_gyo.append(get_standard_deviation(temp, mean))

    xy_cor_gyo = []
    xz_cor_gyo = []
    zy_cor_gyo = []

    for i in xrange(len(x_data_gyo)):

        cor_xy_gyo = get_correlation(x_data_gyo[i], y_data_gyo[i],
                                     x_mean_gyo[i], y_mean_gyo[i],
                                     x_st_deviation_gyo[i], y_st_deviation_gyo[i])

        cor_xz_gyo = get_correlation(x_data_gyo[i], z_data_gyo[i],
                                     x_mean_gyo[i], z_mean_gyo[i],
                                     x_st_deviation_gyo[i], z_st_deviation_gyo[i])

        cor_zy_gyo = get_correlation(z_data_gyo[i], y_data_gyo[i],
                                     z_mean_gyo[i], y_mean_gyo[i],
                                     z_st_deviation_gyo[i], y_st_deviation_gyo[i])

        xy_cor_gyo.append(cor_xy_gyo)
        xz_cor_gyo.append(cor_xz_gyo)
        zy_cor_gyo.append(cor_zy_gyo)

    data = ndarray(shape=(len(subject_data), 21), dtype=float)

    for i in xrange(len(x_data)):

        data[i] = array([x_mean[i], x_energy[i], x_st_deviation[i],
                         y_mean[i], y_energy[i], y_st_deviation[i],
                         z_mean[i], z_energy[i], z_st_deviation[i],
                         xy_cor[i], xz_cor[i], zy_cor[i],
                         x_mean_gyo[i], x_st_deviation_gyo[i],
                         y_mean_gyo[i], y_st_deviation_gyo[i],
                         z_mean_gyo[i], z_st_deviation_gyo[i],
                         xy_cor_gyo[i], xz_cor_gyo[i], zy_cor_gyo[i]])

    return target, data


def load_data_enhanced(results_filename,
                       acc_x_filename, acc_y_filename, acc_z_filename,
                       gyo_x_filename, gyo_y_filename, gyo_z_filename):

    subject = open(results_filename, 'r')
    subject_data = []

    for line in subject:
        subject_data.append(int(line))

    target = ndarray(shape=(len(subject_data),), dtype=int, buffer=array(subject_data))

    x_data = []
    x_mean = []
    x_energy = []
    x_min = []
    x_max = []
    x_mad = []
    x_st_deviation = []

    x_file = open(acc_x_filename, 'r')

    for line in x_file:
        x_values = line.split(',')
        temp = []
        for value in x_values:
            temp.append(float(value))
        mean = get_mean(temp)

        x_data.append(temp)
        x_mean.append(mean)
        x_energy.append(get_energy(temp))
        x_min.append(get_min(temp))
        x_max.append(get_max(temp))
        x_mad.append(get_mad(temp, mean))
        x_st_deviation.append(get_standard_deviation(temp, mean))

    y_data = []
    y_mean = []
    y_energy = []
    y_min = []
    y_max = []
    y_mad = []
    y_st_deviation = []

    y_file = open(acc_y_filename, 'r')

    for line in y_file:
        y_values = line.split(',')
        temp = []
        for value in y_values:
            temp.append(float(value))
        mean = get_mean(temp)

        y_data.append(temp)
        y_mean.append(mean)
        y_energy.append(get_energy(temp))
        y_min.append(get_min(temp))
        y_max.append(get_max(temp))
        y_mad.append(get_mad(temp, mean))
        y_st_deviation.append(get_standard_deviation(temp, mean))

    z_data = []
    z_mean = []
    z_energy = []
    z_min = []
    z_max = []
    z_mad = []
    z_st_deviation = []

    z_file = open(acc_z_filename, 'r')

    for line in z_file:
        z_values = line.split(',')
        temp = []
        for value in z_values:
            temp.append(float(value))
        mean = get_mean(temp)

        z_data.append(temp)
        z_mean.append(mean)
        z_energy.append(get_energy(temp))
        z_min.append(get_min(temp))
        z_max.append(get_max(temp))
        z_mad.append(get_mad(temp, mean))
        z_st_deviation.append(get_standard_deviation(temp, mean))

    xy_cor = []
    xz_cor = []
    zy_cor = []

    for i in xrange(len(x_data)):

        cor_xy = get_correlation(x_data[i], y_data[i], x_mean[i], y_mean[i], x_st_deviation[i], y_st_deviation[i])
        cor_xz = get_correlation(x_data[i], z_data[i], x_mean[i], z_mean[i], x_st_deviation[i], z_st_deviation[i])
        cor_zy = get_correlation(z_data[i], y_data[i], z_mean[i], y_mean[i], z_st_deviation[i], y_st_deviation[i])

        xy_cor.append(cor_xy)
        xz_cor.append(cor_xz)
        zy_cor.append(cor_zy)

    x_data_gyo = []
    x_mean_gyo = []
    x_min_gyo = []
    x_max_gyo = []
    x_mad_gyo = []
    x_st_deviation_gyo = []

    x_file = open(gyo_x_filename, 'r')

    for line in x_file:
        x_values = line.split(',')
        temp = []
        for value in x_values:
            temp.append(float(value))
        mean = get_mean(temp)

        x_data_gyo.append(temp)
        x_mean_gyo.append(mean)
        x_min_gyo.append(get_min(temp))
        x_max_gyo.append(get_max(temp))
        x_mad_gyo.append(get_mad(temp, mean))
        x_st_deviation_gyo.append(get_standard_deviation(temp, mean))

    y_data_gyo = []
    y_mean_gyo = []
    y_min_gyo = []
    y_max_gyo = []
    y_mad_gyo = []
    y_st_deviation_gyo = []

    y_file = open(gyo_y_filename, 'r')

    for line in y_file:
        y_values = line.split(',')
        temp = []
        for value in y_values:
            temp.append(float(value))
        mean = get_mean(temp)

        y_data_gyo.append(temp)
        y_mean_gyo.append(mean)
        y_min_gyo.append(get_min(temp))
        y_max_gyo.append(get_max(temp))
        y_mad_gyo.append(get_mad(temp, mean))
        y_st_deviation_gyo.append(get_standard_deviation(temp, mean))

    z_data_gyo = []
    z_mean_gyo = []
    z_min_gyo = []
    z_max_gyo = []
    z_mad_gyo = []
    z_st_deviation_gyo = []

    z_file = open(gyo_z_filename, 'r')

    for line in z_file:
        z_values = line.split(',')
        temp = []
        for value in z_values:
            temp.append(float(value))
        mean = get_mean(temp)

        z_data_gyo.append(temp)
        z_mean_gyo.append(mean)
        z_min_gyo.append(get_min(temp))
        z_max_gyo.append(get_max(temp))
        z_mad_gyo.append(get_mad(temp, mean))
        z_st_deviation_gyo.append(get_standard_deviation(temp, mean))

    xy_cor_gyo = []
    xz_cor_gyo = []
    zy_cor_gyo = []

    for i in xrange(len(x_data_gyo)):

        cor_xy_gyo = get_correlation(x_data_gyo[i], y_data_gyo[i],
                                     x_mean_gyo[i], y_mean_gyo[i],
                                     x_st_deviation_gyo[i], y_st_deviation_gyo[i])

        cor_xz_gyo = get_correlation(x_data_gyo[i], z_data_gyo[i],
                                     x_mean_gyo[i], z_mean_gyo[i],
                                     x_st_deviation_gyo[i], z_st_deviation_gyo[i])

        cor_zy_gyo = get_correlation(z_data_gyo[i], y_data_gyo[i],
                                     z_mean_gyo[i], y_mean_gyo[i],
                                     z_st_deviation_gyo[i], y_st_deviation_gyo[i])

        xy_cor_gyo.append(cor_xy_gyo)
        xz_cor_gyo.append(cor_xz_gyo)
        zy_cor_gyo.append(cor_zy_gyo)

    data = ndarray(shape=(len(subject_data), 39), dtype=float)

    for i in xrange(len(x_data)):

        data[i] = array([x_mean[i], x_energy[i], x_st_deviation[i],
                         x_min[i], x_max[i], x_mad[i],
                         y_mean[i], y_energy[i], y_st_deviation[i],
                         y_min[i], y_max[i], y_mad[i],
                         z_mean[i], z_energy[i], z_st_deviation[i],
                         z_min[i], z_max[i], z_mad[i],
                         xy_cor[i], xz_cor[i], zy_cor[i],
                         x_mean_gyo[i], x_st_deviation_gyo[i],
                         x_min_gyo[i], x_max_gyo[i], x_mad_gyo[i],
                         y_mean_gyo[i], y_st_deviation_gyo[i],
                         y_min_gyo[i], y_max_gyo[i], y_mad_gyo[i],
                         z_mean_gyo[i], z_st_deviation_gyo[i],
                         z_min_gyo[i], z_max_gyo[i], z_mad_gyo[i],
                         xy_cor_gyo[i], xz_cor_gyo[i], zy_cor_gyo[i]])

    return target, data