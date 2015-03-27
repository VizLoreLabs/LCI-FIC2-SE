from math import sqrt
from numpy import ndarray, array


def get_mean(x_array):
    """
    Calculates the mean of the array
    :param x_array:
    :return:
    """
    return sum(x_array) / len(x_array)


def get_standard_deviation(x_array, mean):
    """
    Calculates the standard deviation of the array
    :param x_array:
    :param mean:
    :return:
    """
    s = 0
    for i in xrange(len(x_array)):
        s += (x_array[i] - mean)**2
    return sqrt(s / len(x_array))


def get_energy(x_array):
    """
    Calculates the energy of the array
    :param x_array:
    :return:
    """
    s = 0
    for i in xrange(len(x_array)):
        s += x_array[i]**2
    return s / len(x_array)


def get_correlation(x_array, y_array, x_mean, y_mean, x_sd, y_sd):
    """
    Calculates the correlation between the x_array and the y_array
    :param x_array:
    :param y_array:
    :param x_mean:
    :param y_mean:
    :param x_sd:
    :param y_sd:
    :return:
    """
    s = 0
    for i in range(len(x_array)):
        s += (x_array[i] - x_mean)*(y_array[i] - y_mean)
    return s / (len(x_array)*x_sd*y_sd)


def get_min(x_array):
    """
    Gets the minimum of the x_array
    :param x_array:
    :return:
    """
    return min(x_array)


def get_max(x_array):
    """
    Gets the maximum of the x_array
    :param x_array:
    :return:
    """
    return max(x_array)


def get_mad(x_array, x_mean):
    """
    Gets the mean absolute deviation
    :param x_array:
    :param x_mean:
    :return:
    """
    x_m_array = []
    for value in x_array:
        x_m_array.append(abs(value - x_mean))
    return get_mean(x_m_array)


def get_features(x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo):
    
    """
    Gets the features required to do the standard activity recognition
    :param x_acc:
    :param y_acc:
    :param z_acc:
    :param x_gyo:
    :param y_gyo:
    :param z_gyo:
    :return:
    """
    x_acc_mean = get_mean(x_acc)
    y_acc_mean = get_mean(y_acc)
    z_acc_mean = get_mean(z_acc)
    
    x_gyo_mean = get_mean(x_gyo)
    y_gyo_mean = get_mean(y_gyo)
    z_gyo_mean = get_mean(z_gyo)
    
    x_acc_energy = get_energy(x_acc)
    y_acc_energy = get_energy(y_acc)
    z_acc_energy = get_energy(z_acc)
    
    x_acc_std_dev = get_standard_deviation(x_acc, x_acc_mean)
    y_acc_std_dev = get_standard_deviation(y_acc, y_acc_mean)
    z_acc_std_dev = get_standard_deviation(z_acc, z_acc_mean)
    
    x_gyo_std_dev = get_standard_deviation(x_gyo, x_gyo_mean)
    y_gyo_std_dev = get_standard_deviation(y_gyo, y_gyo_mean)
    z_gyo_std_dev = get_standard_deviation(z_gyo, z_gyo_mean)
    
    xy_acc_cor = get_correlation(x_acc, y_acc, x_acc_mean, y_acc_mean, x_acc_std_dev, y_acc_std_dev)
    xz_acc_cor = get_correlation(x_acc, z_acc, x_acc_mean, z_acc_mean, x_acc_std_dev, z_acc_std_dev)
    zy_acc_cor = get_correlation(z_acc, y_acc, z_acc_mean, y_acc_mean, z_acc_std_dev, y_acc_std_dev)    
    
    xy_gyo_cor = get_correlation(x_gyo, y_gyo, x_gyo_mean, y_gyo_mean, x_gyo_std_dev, y_gyo_std_dev)
    xz_gyo_cor = get_correlation(x_gyo, z_gyo, x_gyo_mean, z_gyo_mean, x_gyo_std_dev, z_gyo_std_dev)
    zy_gyo_cor = get_correlation(z_gyo, y_gyo, z_gyo_mean, y_gyo_mean, z_gyo_std_dev, y_gyo_std_dev)

    data = ndarray(shape=(1, 21), dtype=float)
    data[0] = array([x_acc_mean, x_acc_energy, x_acc_std_dev,
                     y_acc_mean, y_acc_energy, y_acc_std_dev,
                     z_acc_mean, z_acc_energy, z_acc_std_dev,
                     xy_acc_cor, xz_acc_cor, zy_acc_cor,
                     x_gyo_mean, x_gyo_std_dev,
                     y_gyo_mean, y_gyo_std_dev,
                     z_gyo_mean, z_gyo_std_dev,
                     xy_gyo_cor, xz_gyo_cor, zy_gyo_cor])
    return data


def get_features_acceleration(x_acc, y_acc, z_acc):

    """
    Gets the features required to do the activity recognition using only the acceleration data
    :param x_acc:
    :param y_acc:
    :param z_acc:
    :return:
    """
    x_acc_mean = get_mean(x_acc)
    y_acc_mean = get_mean(y_acc)
    z_acc_mean = get_mean(z_acc)

    x_acc_energy = get_energy(x_acc)
    y_acc_energy = get_energy(y_acc)
    z_acc_energy = get_energy(z_acc)

    x_acc_std_dev = get_standard_deviation(x_acc, x_acc_mean)
    y_acc_std_dev = get_standard_deviation(y_acc, y_acc_mean)
    z_acc_std_dev = get_standard_deviation(z_acc, z_acc_mean)

    xy_acc_cor = get_correlation(x_acc, y_acc, x_acc_mean, y_acc_mean, x_acc_std_dev, y_acc_std_dev)
    xz_acc_cor = get_correlation(x_acc, z_acc, x_acc_mean, z_acc_mean, x_acc_std_dev, z_acc_std_dev)
    zy_acc_cor = get_correlation(z_acc, y_acc, z_acc_mean, y_acc_mean, z_acc_std_dev, y_acc_std_dev)

    data = ndarray(shape=(1, 12), dtype=float)
    data[0] = array([x_acc_mean, x_acc_energy, x_acc_std_dev,
                     y_acc_mean, y_acc_energy, y_acc_std_dev,
                     z_acc_mean, z_acc_energy, z_acc_std_dev,
                     xy_acc_cor, xz_acc_cor, zy_acc_cor])
    return data


def get_enhanced_features(x_acc, y_acc, z_acc, x_gyo, y_gyo, z_gyo):

    """
    Gets the features required to do the enhanced activity recognition using only the acceleration data
    :param x_acc:
    :param y_acc:
    :param z_acc:
    :param x_gyo:
    :param y_gyo:
    :param z_gyo:
    :return:
    """
    x_acc_mean = get_mean(x_acc)
    y_acc_mean = get_mean(y_acc)
    z_acc_mean = get_mean(z_acc)

    x_acc_min = get_min(x_acc)
    y_acc_min = get_min(y_acc)
    z_acc_min = get_min(z_acc)
    
    x_acc_max = get_max(x_acc)
    y_acc_max = get_max(y_acc)
    z_acc_max = get_max(z_acc)
    
    x_acc_mad = get_mad(x_acc, x_acc_mean)
    y_acc_mad = get_mad(y_acc, y_acc_mean)
    z_acc_mad = get_mad(z_acc, z_acc_mean)

    x_gyo_mean = get_mean(x_gyo)
    y_gyo_mean = get_mean(y_gyo)
    z_gyo_mean = get_mean(z_gyo)

    x_gyo_min = get_min(x_gyo)
    y_gyo_min = get_min(y_gyo)
    z_gyo_min = get_min(z_gyo)
    
    x_gyo_max = get_max(x_gyo)
    y_gyo_max = get_max(y_gyo)
    z_gyo_max = get_max(z_gyo)
    
    x_gyo_mad = get_mad(x_gyo, x_gyo_mean)
    y_gyo_mad = get_mad(y_gyo, y_gyo_mean)
    z_gyo_mad = get_mad(z_gyo, z_gyo_mean)

    x_acc_energy = get_energy(x_acc)
    y_acc_energy = get_energy(y_acc)
    z_acc_energy = get_energy(z_acc)

    x_acc_std_dev = get_standard_deviation(x_acc, x_acc_mean)
    y_acc_std_dev = get_standard_deviation(y_acc, y_acc_mean)
    z_acc_std_dev = get_standard_deviation(z_acc, z_acc_mean)

    x_gyo_std_dev = get_standard_deviation(x_gyo, x_gyo_mean)
    y_gyo_std_dev = get_standard_deviation(y_gyo, y_gyo_mean)
    z_gyo_std_dev = get_standard_deviation(z_gyo, z_gyo_mean)

    xy_acc_cor = get_correlation(x_acc, y_acc, x_acc_mean, y_acc_mean, x_acc_std_dev, y_acc_std_dev)
    xz_acc_cor = get_correlation(x_acc, z_acc, x_acc_mean, z_acc_mean, x_acc_std_dev, z_acc_std_dev)
    zy_acc_cor = get_correlation(z_acc, y_acc, z_acc_mean, y_acc_mean, z_acc_std_dev, y_acc_std_dev)

    xy_gyo_cor = get_correlation(x_gyo, y_gyo, x_gyo_mean, y_gyo_mean, x_gyo_std_dev, y_gyo_std_dev)
    xz_gyo_cor = get_correlation(x_gyo, z_gyo, x_gyo_mean, z_gyo_mean, x_gyo_std_dev, z_gyo_std_dev)
    zy_gyo_cor = get_correlation(z_gyo, y_gyo, z_gyo_mean, y_gyo_mean, z_gyo_std_dev, y_gyo_std_dev)

    data = ndarray(shape=(1, 39), dtype=float)

    data[0] = array([x_acc_mean, x_acc_energy, x_acc_std_dev,
                     x_acc_min, x_acc_max, x_acc_mad,
                     y_acc_mean, y_acc_energy, y_acc_std_dev,
                     y_acc_min, y_acc_max, y_acc_mad,
                     z_acc_mean, z_acc_energy, z_acc_std_dev,
                     z_acc_min, z_acc_max, z_acc_mad,
                     xy_acc_cor, xz_acc_cor, zy_acc_cor,
                     x_gyo_mean, x_gyo_std_dev,
                     x_gyo_min, x_gyo_max, x_gyo_mad,
                     y_gyo_mean, y_gyo_std_dev,
                     y_gyo_min, y_gyo_max, y_gyo_mad,
                     z_gyo_mean, z_gyo_std_dev,
                     z_gyo_min, z_gyo_max, z_gyo_mad,
                     xy_gyo_cor, xz_gyo_cor, zy_gyo_cor])
    return data


def get_enhanced_features_acceleration(x_acc, y_acc, z_acc):

    """

    :param x_acc:
    :param y_acc:
    :param z_acc:
    :return:
    """
    x_acc_mean = get_mean(x_acc)
    y_acc_mean = get_mean(y_acc)
    z_acc_mean = get_mean(z_acc)

    x_acc_min = get_min(x_acc)
    y_acc_min = get_min(y_acc)
    z_acc_min = get_min(z_acc)

    x_acc_max = get_max(x_acc)
    y_acc_max = get_max(y_acc)
    z_acc_max = get_max(z_acc)

    x_acc_mad = get_mad(x_acc, x_acc_mean)
    y_acc_mad = get_mad(y_acc, y_acc_mean)
    z_acc_mad = get_mad(z_acc, z_acc_mean)

    x_acc_energy = get_energy(x_acc)
    y_acc_energy = get_energy(y_acc)
    z_acc_energy = get_energy(z_acc)

    x_acc_std_dev = get_standard_deviation(x_acc, x_acc_mean)
    y_acc_std_dev = get_standard_deviation(y_acc, y_acc_mean)
    z_acc_std_dev = get_standard_deviation(z_acc, z_acc_mean)

    xy_acc_cor = get_correlation(x_acc, y_acc, x_acc_mean, y_acc_mean, x_acc_std_dev, y_acc_std_dev)
    xz_acc_cor = get_correlation(x_acc, z_acc, x_acc_mean, z_acc_mean, x_acc_std_dev, z_acc_std_dev)
    zy_acc_cor = get_correlation(z_acc, y_acc, z_acc_mean, y_acc_mean, z_acc_std_dev, y_acc_std_dev)

    data = ndarray(shape=(1, 21), dtype=float)

    data[0] = array([x_acc_mean, x_acc_energy, x_acc_std_dev,
                     x_acc_min, x_acc_max, x_acc_mad,
                     y_acc_mean, y_acc_energy, y_acc_std_dev,
                     y_acc_min, y_acc_max, y_acc_mad,
                     z_acc_mean, z_acc_energy, z_acc_std_dev,
                     z_acc_min, z_acc_max, z_acc_mad,
                     xy_acc_cor, xz_acc_cor, zy_acc_cor])
    return data