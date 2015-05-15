""" This file contains all functions that works with coordinates or with Points of Interest. """
import urllib2
import json

from threading import Thread
from math import radians, cos, sin, atan2, sqrt, ceil, pi, floor
from models import Area

""" Global variables """
EARTH_RADIUS = 6371500
EARTH_CIRCUMFERENCE = EARTH_RADIUS * pi * 2
EARTH_CIRCUMFERENCE_1_2 = EARTH_CIRCUMFERENCE / 2
EARTH_CIRCUMFERENCE_1_4 = EARTH_CIRCUMFERENCE / 4

RADIUS = 300

REC_W = RADIUS
REC_H = RADIUS

LAT_ID_MAX = ceil(EARTH_CIRCUMFERENCE_1_4 / REC_H)
LON_ID_MAX = ceil(EARTH_CIRCUMFERENCE_1_2 / REC_W)

# NOTE: Use your own CLIENT_ID and CLIENT_SECRET to communicate with Foursquare.
CLIENT_ID = "PHLMPJ4EJZB2QBQHZG2KUUTNNWZTLW4ZEJRRQI5VW5TLMRMI"
CLIENT_SECRET = "A25MIXXIPP42RD1P4T4PMKZVIYE0OAUHHWX1PPB3YECAFQ4N"

BASE_URL = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&limit=50&intent=browse"\
           % (CLIENT_ID, CLIENT_SECRET)

POI_DP_URL = "http://localhost/poi_dp/"

# Testing data used for Barcelona demonstration event.
ref_cat = {
    'Lunch': [

        '4bf58dd8d48988d147941735', '4bf58dd8d48988d117941735', '4bf58dd8d48988d1c4941735',
        '4bf58dd8d48988d1c0941735', '4bf58dd8d48988d148941735', '4bf58dd8d48988d1db931735',
        '4bf58dd8d48988d1c1941735', '4bf58dd8d48988d1d1941735', '4bf58dd8d48988d1ce941735',
        '4bf58dd8d48988d150941735', '4bf58dd8d48988d16c941735', '4bf58dd8d48988d110941735',
        '4f04af1f2fb6e1c99f3db0bb', '4bf58dd8d48988d17a941735', '4bf58dd8d48988d1c3941735',
        '4bf58dd8d48988d1d2941735', '4bf58dd8d48988d111941735', '4bf58dd8d48988d1df931735',
        '4bf58dd8d48988d1cb941735', '4bf58dd8d48988d16e941735', '4bf58dd8d48988d16f941735',
        '4bf58dd8d48988d1ca941735', '4bf58dd8d48988d142941735', '4bf58dd8d48988d16a941735',
        '52e81612bcbc57f1066b79f1', '52e81612bcbc57f1066b7a00', '5283c7b4e4b094cb91ec88d7',
        '4bf58dd8d48988d1c7941735', '4bf58dd8d48988d150941735', '4bf58dd8d48988d1bd941735',
        '4bf58dd8d48988d1a1941735', '4bf58dd8d48988d148941735', '4bf58dd8d48988d1d0941735',
        '5283c7b4e4b094cb91ec88d4', '4bf58dd8d48988d1db931735'
    ],

    'Club and bar': [
        '4bf58dd8d48988d14b941735', '4bf58dd8d48988d117941735', '4bf58dd8d48988d11a941735',
        '4bf58dd8d48988d116941735', '50327c8591d4c4b30a586d5d', '4bf58dd8d48988d1ca941735',
        '4bf58dd8d48988d123951735', '4bf58dd8d48988d1c7941735', '4bf58dd8d48988d18e941735',
        '4bf58dd8d48988d1e5931735', '4bf58dd8d48988d11e941735', '4bf58dd8d48988d11f941735'
    ],

    'Transport': [
        '4bf58dd8d48988d1fd931735', '52f2ab2ebcbc57f1066b8b51', '4bf58dd8d48988d1fe931735',
        '4bf58dd8d48988d12b951735', '4bf58dd8d48988d130951735', '4e4c9077bd41f78e849722f9'
    ],

    'Entertainment': [
        '4bf58dd8d48988d137941735', '4bf58dd8d48988d181941735', '52e81612bcbc57f1066b79ee',
        '4deefb944765f83613cdba6e', '4bf58dd8d48988d1e7941735', '4bf58dd8d48988d1e2931735',
        '4bf58dd8d48988d164941735', '52e81612bcbc57f1066b7a25', '4bf58dd8d48988d12f941735',
        '4bf58dd8d48988d191941735', '4bf58dd8d48988d163941735', '4bf58dd8d48988d1fd941735',
        '4bf58dd8d48988d15e941735', '4bf58dd8d48988d1ed941735', '4bf58dd8d48988d1e5931735',
        '4bf58dd8d48988d1e5941735', '4bf58dd8d48988d17f941735', '4bf58dd8d48988d1c9941735'
    ],

    'Morning': [
        '4bf58dd8d48988d1e0931735', '4bf58dd8d48988d147941735', '4bf58dd8d48988d16d941735',
        '4bf58dd8d48988d143941735', '4c38df4de52ce0d596b336e1', '4bf58dd8d48988d175941735',
        '4bf58dd8d48988d1c5941735', '4bf58dd8d48988d16a941735', '4bf58dd8d48988d1e5941735',
        '4bf58dd8d48988d148941735']
}


class GetFoursquareResponses(Thread):
    """
    This class is representing one thread sending request to Foursquare API and then processing received data and
    storing the data to POI Data Provider database.
    """
    def __init__(self, key, ne_lat, ne_lng, sw_lat, sw_lng):
        self.results = []
        self.key = key
        self.ne_lat = ne_lat
        self.ne_lng = ne_lng
        self.sw_lat = sw_lat
        self.sw_lng = sw_lng
        super(GetFoursquareResponses, self).__init__()

    def run(self):
        raw_data = extend(self.sw_lng, self.sw_lat, self.ne_lng, self.ne_lat, ref_cat[self.key])

        for row in raw_data:
            info = {"fw_core": {"location": {"wgs84": {"latitude": row['geometry']['coordinates'][1],
                                                       "longitude": row['geometry']['coordinates'][0]}},
                                "category": self.key,
                                "name": {"": row['properties']['name']},
                                "short_name": {"": row['properties']['name']},
                                "label": {"": row['properties']['category']},
                                "source": "foursquare"
                                }
                    }
            self.results.append(info)


class GetGivenRectangles(Thread):
    """
    This class represents thread requesting POIs for given area.
    """
    def __init__(self, area_id):
        self.results = []
        self.area_id = area_id
        super(GetGivenRectangles, self).__init__()

    def run(self):
        sw_ne = get_sw_ne(self.area_id)
        self.results.append(
            get_points_ne_sw(sw_ne['ne']['lat'], sw_ne['ne']['lng'], sw_ne['sw']['lat'], sw_ne['sw']['lng'], None)
        )

        # Store given rectangle as existing to database.
        Area(lat_id=self.area_id['lat'], lng_id=self.area_id['lng']).save()


def get_response(url):
    """
    This function is used to make connection to Foursquare API.
    :param url: String representation of URL that user wants to call.
    :return: Return dictionary of venues from Foursquare API
    """
    headers = dict()
    headers['Accept'] = 'application/json'
    request = urllib2.Request(url, None, headers)
    result = urllib2.urlopen(request)
    obj = json.loads(result.read())
    poi = obj['response']['venues']
    return poi


def filter_result(data):
    """
    Filters the result that Foursquare API returned as answer to our request. Filtered result is compatible with POI
    proxy Specific Enabler that can be used to collect data from different online services.
    NOTE: There code is available on https://github.com/alrocar/POIProxy .
    :param data: Dictionary of venues returned from Foursquare API.
    :return: Returns new dictionary containing only one part of information from original response.
    """
    new_data = []
    for poi in data:
        new_data.append({"geometry": {"coordinates": [poi['location']['lng'], poi['location']['lat']]},
                         "properties": {"name": poi['name'], "category": poi['categories'][0]['name']}})
    return new_data


def radius(lat, lon, dist, categories=None, search=None):
    """
    Defines how to use radius search on Foursquare API. User just needs to provide data, everything else will be
    modified as defined on Foursquare API.
    :param lat: Latitude of center point.
    :param lon: Longitude of center point.
    :param dist: Distance from center point defining a search region.
    :param categories: POI categories that we are interested in.
    :param search: Search term in form of string. NOTE: No spaces!
    :return: Filtered result from Foursquare API.
    """
    if search is None:
        url = BASE_URL + "&radius=%d&v=20150101&ll=%f,%f" % (dist, lat, lon)
    else:
        url = BASE_URL + "&radius=%d&v=20150101&ll=%f,%f&search=%s" % (dist, lat, lon, search)

    if categories is not None:
        url_add = ""
        for cat in categories:
            url_add = url_add + str(cat) + ","

        url = url + "&categoryId=" + url_add
        url = url[:-1]

    poi = get_response(url)
    return filter_result(poi)


def extend(min_x, min_y, max_x, max_y, categories=None, search=None):
    """
    Defines how to use radius search on Foursquare API. User just needs to provide data, everything else will be
    modified as defined on Foursquare API.
    :param min_x: Longitude of South-West point.
    :param min_y: Latitude of South-West point.
    :param max_x: Longitude Requested setting DEFAULT_INDEX_TABLESPACE, but settings are not configured. You must either
     define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings of
      North-East point.
    :param max_y: Longitude of North-East point.
    :param categories: POI categories that we are interested in.
    :param search: Search term in form of string. NOTE: No spaces!
    :return: Filtered result from Foursquare API.
    """
    if search is None:
        url = BASE_URL + "&v=20150101&sw=%f,%f&ne=%f,%f" % (min_y, min_x, max_y, max_x)
    else:
        url = BASE_URL + "&v=20150101&sw=%f,%f&ne=%f,%f&search=%s" % (min_y, min_x, max_y, max_x, search)

    if categories is not None:
        url_add = ""
        for cat in categories:
            url_add = url_add + str(cat) + ","

        url = url + "&categoryId=" + url_add
        url = url[:-1]

    poi = get_response(url)
    return filter_result(poi)


def distance_between_gps_coordinates(lat_a, lon_a, lat_b, lon_b):
    """
    Calculate the distance in meters between two GPS points.
    :param lat_a: Latitude of point A.
    :param lon_a: Longitude of point A.
    :param lat_b: Latitude of point B.
    :param lon_b: Longitude of point B.
    :return: Distance between two given points in meters.
    """
    d_lon = radians(lon_b - lon_a)
    d_lat = radians(lat_b - lat_a)
    a = ((sin(d_lat/2)) ** 2) + cos(radians(lat_a)) * cos(radians(lat_b)) * ((sin(d_lon/2)) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return EARTH_RADIUS * c


def grade_distance(lat_a, lng_a, lat_b, lng_b):
    """
    Gives grades for every distance, smaller distance gives better grade.
    :param lat_a: Latitude of point A.
    :param lng_a: Longitude of point A.
    :param lat_b: Latitude of point B.
    :param lng_b: Longitude of point B.
    :return: Returns grade for given distance.
    """
    dist = distance_between_gps_coordinates(lat_a, lng_a, lat_b, lng_b)
    if dist <= 10:
        return 5
    elif dist <= 50:
        return 3
    elif dist <= 200:
        return 2
    else:
        return 1


def get_id(coordinates):
    """
    Coordinates are processed and based on them function returns identification for this coordinates.
    :param coordinates: Dictionary on latitude and longitude coordinates of given point.
    :return: Dictionary of latitude and longitude identification numbers for processed rectangle.
    """
    lat_id = floor(EARTH_CIRCUMFERENCE_1_4 * coordinates['lat'] / 90 / REC_H)
    lat = 90 * lat_id / EARTH_CIRCUMFERENCE_1_4 * REC_H
    lng_id = floor(EARTH_CIRCUMFERENCE_1_2 * cos(radians(lat)) * coordinates['lng'] / 180 / REC_W)
    return {'lat': lat_id, 'lng': lng_id}


def get_sw_ne(db_id):
    """
    Based on rectangle identification, function returns South-West and North-East points describing that rectangle.
    :param db_id: Rectangle identification dictionary, containing two numbers.
    :return: Dictionary containing two coordinate dictionaries.
    """
    lat_s = 90 * db_id['lat'] / EARTH_CIRCUMFERENCE_1_4 * REC_H
    lng_w = 180 * db_id['lng'] / (EARTH_CIRCUMFERENCE_1_2 * cos(radians(lat_s))) * REC_W
    lat_n = 90 * (db_id['lat'] + 1) / EARTH_CIRCUMFERENCE_1_4 * REC_H
    lng_e = 180 * (db_id['lng'] + 1) / (EARTH_CIRCUMFERENCE_1_2 * cos(radians(lat_s))) * REC_W
    return {'sw': {'lat': lat_s, 'lng': lng_w}, 'ne': {'lat': lat_n, 'lng': lng_e}}


def distance(point_a, point_b):
    """
    Calculates distance between two GPS points described with two dictionaries.
    :param point_a: Dictionary containing latitude and longitude of given point.
    :param point_b: Dictionary containing latitude and longitude of given point.
    :return: Distance between points in meters.
    """
    d_lng = radians(point_b['lng'] - point_a['lng'])
    d_lat = radians(point_b['lat'] - point_a['lat'])
    a = sin(d_lat/2)**2 + cos(radians(point_a['lat'])) * cos(radians(point_b['lat'])) * sin(d_lng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return EARTH_RADIUS * c


def center(rect):
    """
    Calculate coordinates of central point inside given rectangle.
    :param rect: Dictionary representing North-East and South-West points of given rectangle area.
    :return: Dictionary (containing latitude and longitude) describing central point of given rectangle area.
    """
    return {'lat': (rect['sw']['lat'] + rect['ne']['lat']) / 2, 'lng': (rect['sw']['lng'] + rect['ne']['lng']) / 2}


def get_ids(coordinates):
    """
    For given coordinates returns rectangle identification dictionaries that are candidates for circle intersection.
    :param coordinates: Dictionary containing latitude and longitude of some point.
    :return: List of dictionaries that represent nine rectangles that are candidates for circle intersection.
    """
    size = int (ceil(float(RADIUS) / min(REC_H, REC_W)))
    ids = []
    center_id = get_id(coordinates)
    center_sq = get_sw_ne(center_id)

    lat_dh = (center_sq['ne']['lat'] - center_sq['sw']['lat']) / 2

    ids.append(center_id)
    for j in range(1, size + 1):
        # West
        identification = {'lat': center_id['lat'], 'lng': center_id['lng'] - j}
        sq = get_sw_ne(identification)
        if distance(coordinates, center(sq)) <= RADIUS:
            ids.append(identification)

        # East
        identification = {'lat': center_id['lat'], 'lng': center_id['lng'] + j}
        sq = get_sw_ne(identification)
        if distance(coordinates, center(sq)) <= RADIUS:
            ids.append(identification)

        top_sq = center_sq.copy()
        bot_sq = center_sq.copy()

    for i in range(0, size):
        top_id = get_id({'lat': top_sq['ne']['lat'] + lat_dh, 'lng': coordinates['lng']})
        bot_id = get_id({'lat': bot_sq['sw']['lat'] - lat_dh, 'lng': coordinates['lng']})
        top_sq = get_sw_ne(top_id)
        bot_sq = get_sw_ne(bot_id)
        if distance(coordinates, center(top_sq)) <= RADIUS:
            ids.append(top_id)

        if distance(coordinates, center(bot_sq)) <= RADIUS:
            ids.append(bot_id)

        for j in range(1, size + 1):
            # North-West
            identification = {'lat': top_id['lat'], 'lng': top_id['lng'] - j}
            sq = get_sw_ne(identification)
            if distance(coordinates, center(sq)) <= RADIUS:
                ids.append(identification)

            # North-East
            identification = {'lat': top_id['lat'], 'lng': top_id['lng'] + j}
            sq = get_sw_ne(identification)
            if distance(coordinates, center(sq)) <= RADIUS:
                ids.append(identification)

            # South-West
            identification = {'lat': bot_id['lat'], 'lng': bot_id['lng'] - j}
            sq = get_sw_ne(identification)
            if distance(coordinates, center(sq)) <= RADIUS:
                ids.append(identification)

            # South-East
            identification = {'lat': bot_id['lat'], 'lng': bot_id['lng'] + j}
            sq = get_sw_ne(identification)
            if distance(coordinates, center(sq)) <= RADIUS:
                ids.append(identification)
    return ids


def get_points_ne_sw(ne_lat, ne_lng, sw_lat, sw_lng, categories):
    """
    Function reads all POIs that are part of given categories and store them to list that is then returned.
    :param ne_lat: North-East latitude.
    :param ne_lng: North-East longitude.
    :param sw_lat: South-West latitude.
    :param sw_lng: South-West longitude.
    :param categories: Identification list of categories required.
    :returns result: List of result from all threads.
    """
    threads = []
    results = []
    for key in ref_cat:
        t = GetFoursquareResponses(key, ne_lat, ne_lng, sw_lat, sw_lng)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        for row in t.results:
            results.append(row)
    return results


def check_for_areas(area_list):
    """
    Check what area fields need to be stored to POI Data Provider, resulting in list of coordinates representing this
    areas.
    :param area_list: List of dictionaries, representing all areas needed for successful search to POI DP.
    :return: List of North-East and South-West points representing this areas.
    """
    lst_needed = []
    for area in area_list:
        if not Area.objects.filter(lat_id=area['lat'], lng_id=area['lng']).exists():
            lst_needed.append(area)
    return lst_needed


def store_to_areas(area_id_list):
    """
    Function that stores information for given area identification. Based of this identification, function gets
    coordinates and then makes call to Foursquare API to collect data and store it to POI Data Provider.
    :param area_id_list: List of area identification numbers.
    """
    threads = []
    results = []
    for area_id in area_id_list:
        t = GetGivenRectangles(area_id)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        for lst in t.results:
            for row in lst:
                results.append(row)
    return results


def fetch_poi(lat, lng, distance):
    """
    Search for points of interest on poi data provider, for the given search radius.
    :param lat: Latitude of center point.
    :param lng: Longitude of center point.
    :param distance: Search radius.
    :return: Returns points of interest database provider answer, dictionary of available points of interest in the
    given radius.
    """
    # Check which area field we need.
    lst_ids = get_ids({'lat': lat, 'lng': lng})
    # For given fields check which are not in database.
    needed_ids = check_for_areas(lst_ids)
    # For those that are not stored in database, call Foursquare and store data, for them.
    poi_list = store_to_areas(needed_ids)

    ''' Make a search in Point od Interest Data Provider for POI-s in given radius. '''
    url = POI_DP_URL + ('/radial_search.php?lat=%f&lon=%f&radius=%d' % (lat, lng, distance))
    headers = dict()
    headers['Content-type'] = 'application/json'
    result = None
    read_list = []
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request, timeout=10).read()
    except:
        return dict()
    poi = json.loads(result)
    if 'pois' in poi and len(poi['pois']) > 0:
        read_list = poi['pois']
    else:
        read_list = dict()

    return [read_list, poi_list]