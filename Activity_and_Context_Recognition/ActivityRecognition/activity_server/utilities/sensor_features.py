from activity_server.utilities.statistics import get_standard_deviation, get_mean, get_energy, get_correlation


def get_acceleration_features(x, y, z):

    x_mean = get_mean(x)
    y_mean = get_mean(y)
    z_mean = get_mean(z)

    x_standard_deviation = get_standard_deviation(x, x_mean)
    y_standard_deviation = get_standard_deviation(y, y_mean)
    z_standard_deviation = get_standard_deviation(z, z_mean)

    x_energy = get_energy(x)
    y_energy = get_energy(y)
    z_energy = get_energy(z)

    xy_correlation = get_correlation(x, y, x_mean, y_mean, x_standard_deviation, y_standard_deviation)
    xz_correlation = get_correlation(x, z, x_mean, z_mean, x_standard_deviation, z_standard_deviation)
    zy_correlation = get_correlation(z, y, z_mean, y_mean, z_standard_deviation, y_standard_deviation)

    return [x_mean, y_mean, z_mean,
            x_standard_deviation, y_standard_deviation, z_standard_deviation,
            xy_correlation, xz_correlation, zy_correlation,
            x_energy, y_energy, z_energy]


def get_gyroscope_features(x, y, z):

    x_mean = get_mean(x)
    y_mean = get_mean(y)
    z_mean = get_mean(z)

    x_standard_deviation = get_standard_deviation(x, x_mean)
    y_standard_deviation = get_standard_deviation(y, y_mean)
    z_standard_deviation = get_standard_deviation(z, z_mean)

    xy_correlation = get_correlation(x, y, x_mean, y_mean, x_standard_deviation, y_standard_deviation)
    xz_correlation = get_correlation(x, z, x_mean, z_mean, x_standard_deviation, z_standard_deviation)
    zy_correlation = get_correlation(z, y, z_mean, y_mean, z_standard_deviation, y_standard_deviation)

    return [x_mean, y_mean, z_mean,
            x_standard_deviation, y_standard_deviation, z_standard_deviation,
            xy_correlation, xz_correlation, zy_correlation]