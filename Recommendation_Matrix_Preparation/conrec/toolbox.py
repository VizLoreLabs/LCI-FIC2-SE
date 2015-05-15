import urllib2
import json
import operator

import requests
import re
import time

from itertools import islice
from threading import Thread
from datetime import datetime, timedelta
from conrec.models import Ignore, Keys
from conrec.poi_module import fetch_poi, grade_distance, distance_between_gps_coordinates, POI_DP_URL

'''                  Walking          Sitting         Standing          Default                  '''
lookup_table = [[[2, 5, 1, 1, 4], [3, 4, 1, 1, 4], [3, 4, 1, 1, 4], [3, 5, 1, 1, 4]],  # Morning
                [[4, 2, 5, 1, 1], [4, 1, 3, 1, 1], [5, 1, 4, 1, 1], [4, 1, 4, 1, 1]],  # Noon
                [[4, 4, 2, 2, 3], [4, 4, 1, 2, 3], [4, 4, 1, 2, 3], [4, 4, 1, 2, 3]],  # Afternoon
                [[3, 1, 5, 4, 4], [2, 1, 4, 4, 4], [2, 1, 4, 4, 4], [2, 1, 4, 4, 4]],  # Evening
                [[1, 1, 1, 5, 5], [1, 1, 1, 4, 5], [1, 1, 1, 4, 5], [1, 1, 1, 4, 5]]]  # Night
'''               [ Free time,    Morning,    Lunch,    Bar,    Transport ]                      '''


class WritePOIToDatabase(Thread):
    """
    This class represents thread requesting POIs for given area.
    """
    def __init__(self, poi_dict):
        self.poi_dict = poi_dict
        super(WritePOIToDatabase, self).__init__()

    def run(self):
        for key in self.poi_dict:
            headers = {'content-type': 'application/json'}
            response = requests.post(POI_DP_URL + 'add_poi.php', data=json.dumps(self.poi_dict[key]), headers=headers)

            if response.status_code == 400:
                string = re.sub('[^A-Za-z0-9| |.]+', '', self.poi_dict[key]['fw_core']['name'].get(""))
                split = string.split()
                self.poi_dict[key]['fw_core']['name'] = {"": split[0] + " " + split[1] + " " + split[2]}
                self.poi_dict[key]['fw_core']['short_name'] = {"": split[0]}

                response = requests.post(POI_DP_URL + 'add_poi.php',
                                         data=json.dumps(self.poi_dict[key]), headers=headers)

                if response.status_code == 200:
                    obj = json.loads(response.text)
                    key = Keys(temp=key, real=obj['created_poi']['uuid'])
                    key.save()
                else:
                    print "Error!"

            elif response.status_code == 200:
                obj = json.loads(response.text)
                key = Keys(temp=key, real=obj['created_poi']['uuid'])
                key.save()


def get_time_section(milliseconds):
    """
    Tells as what part of the day is it. Day is split to several sections like: morning, noon, afternoon,
    evening, night. These are predefined by programmer.
    :param milliseconds: Represents current time, in epoch (from January 1, 1970).
    :return: Number representing concrete part of the day. This number is used to reference to lookup table.
    """
    time_s = datetime.fromtimestamp(milliseconds/1000)
    hours = time_s.hour
    if 11 > hours >= 6:
        return 0  # Morning
    elif 15 > hours >= 11:
        return 1  # Noon
    elif 18 > hours >= 15:
        return 2  # Afternoon
    elif 22 > hours >= 18:
        return 3  # Evening
    else:
        return 4  # Night


def get_curr_activity(prob_dict):
    """
    Figure out what category in dictionary of all categories have the best probability.
    :param prob_dict: Dictionary with categories as keys, and probability as values.
    :return: Number representing recognised category. This number is used to reference to lookup table.
    """
    new_prob = sorted(prob_dict.items(), key=operator.itemgetter(1), reverse=True)
    activity = new_prob[0][0]
    if activity == 'walking':
        return 0
    elif activity == 'sitting':
        return 1
    elif activity == 'standing':
        return 2
    else:
        return 3


def decode_activity(act):
    """
    Transforms integer representation of categories to string representation.
    :param act: Number representing one of categories.
    :return: String of recognised activity.
    """
    if act == 0:
        return "walking"
    elif act == 1:
        return "sitting"
    elif act == 2:
        return "standing"
    else:
        return "not recognised"


def get_user_activity(user_id):
    """
    Asks the activity recognition provider what is the current activity for the given user.
    :param user_id: String representation of user unique identification number.
    :return: Returns answer from activity recognition provider.
    """
    url = 'http://activityrq:8089/ac/?ac=1&uuid=%s&alg=svm&fs=standard&tp=600' % user_id
    headers = dict()
    headers['Accept'] = 'application/json'
    result = None

    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request).read()
        activity = json.loads(result)
        return activity
    except(urllib2.HTTPError, urllib2.URLError, Exception):
        return {"error": "Could not contact the server"}


def get_poi(lat, lng, radius):
    """
    Search for points of interest on poi data provider, for the given search radius.
    :param lat: Latitude of center point.
    :param lng: Longitude of center point.
    :param radius: Search radius.
    :return: Returns points of interest database provider answer, dictionary of available points of interest in the
    given radius.
    """
    url = 'http://104.154.38.236/poi_dp/radial_search.php?lat=%f&lon=%f&radius=%d' % (lat, lng, radius)
    headers = dict()
    headers['Content-type'] = 'application/json'
    result = None
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request, timeout=10).read()
    except:
        return dict()
    poi = json.loads(result)
    if 'pois' in poi and len(poi['pois']) > 0:
        return poi['pois']
    else:
        return dict()


def decode_category(category):
    """
    For some given category, already defined by programmer transforms string representation of category to integer
    representation. This integer representation is later used to reference to lookup table.
    :param category: String representation of category.
    :return: Integer representation of the given category.
    """
    if category == 'Entertainment':
        return 0
    elif category == 'Morning':
        return 1
    elif category == 'Lunch':
        return 2
    elif category == 'Club and bar':
        return 3
    elif category == 'Transport':
        return 4
    else:
        return 0


def grade_distance(lat_a, lng_a, lat_b, lng_b):
    """
    Gives grades for every distance, smaller distance gives better grade.
    :param lat_a: Latitude of point A.
    :param lng_a: Longitude of point A.
    :param lat_b: Latitude of point B.
    :param lng_b: Longitude of point B.
    :return: Returns grade for given distance.
    """
    distance = distance_between_gps_coordinates(lat_a, lng_a, lat_b, lng_b)
    if distance <= 10:
        return 5
    elif distance <= 50:
        return 3
    elif distance <= 200:
        return 2
    else:
        return 1


def save_ignored_for_current_user(user_id, poi_id):
    """
    Saves the tuple (user, poi) to local database.
    :param user_id: User identification.
    :param poi_id: POI identification.
    """
    i_poi = Ignore(uuid=user_id, ignored=poi_id)
    i_poi.save()


def get_ignored_for_current_user(user_id):
    """
    Reads what POIs are ignored, from the database.
    :param user_id: User identification.
    :return: List of POI identification, that are already ignored by user.
    """
    lst_ignored = []
    if Ignore.objects.filter(uuid=user_id).exists():
        i_poi = Ignore.objects.all().filter(uuid=user_id)
        for poi in i_poi:
            lst_ignored.append(poi.ignored)
    return lst_ignored


def make_chunks(dictionary, n):
    """
    Function making chunks from given list. Number of chunks is defined by parameter.
    :param dictionary: Data dictionary.
    :param n: Number of chunks to be created.
    :return: Returns generator generating list of dictionaries.
    """
    it = iter(dictionary)
    for k in xrange(0, len(dictionary), n):
        yield {k: dictionary[k] for k in islice(it, n)}


def get_recommendation(time_stamp, coordinates, user_id, ignore):
    """
    Main handler function for recommend.
    :param time_stamp: Time from beginning of the epoch (1.1.1970)
    :param coordinates: Dictionary with coordinates.
    :param user_id: Identification of the current user.
    :param ignore: Identification of POI user ignored from previous recommend.
    :return: Dictionary representing answer for request to recommend.
    """

    ''' Get all POIs in radius of 300 meters from user. '''

    points_of_interest = fetch_poi(coordinates['lat'], coordinates['lon'], 300)

    # First we have to assign writing jobs to threads.
    length = len(points_of_interest[1])
    poi_dict = dict()

    # Add temporary keys and merge the two dictionaries.
    poi_lst_of_dict = points_of_interest[0]
    poi_lst_foursquare = dict()

    for i in range(0, length):
        poi_lst_foursquare['some-temporary-key-%s %d' % (user_id, (i+1))] = points_of_interest[1][i]

    chunk_lst = make_chunks(poi_lst_foursquare, int(length/15) + 1)

    threads = []
    for chunk in chunk_lst:
        t = WritePOIToDatabase(chunk)
        threads.append(t)
        t.start()

    poi_lst_of_dict.update(poi_lst_foursquare)

    ''' Get all required data. '''
    part_of_day = get_time_section(time_stamp)

    act_rest_answer = get_user_activity(user_id)
    if 'error' in act_rest_answer:
        activity = 3  # If activity recognition provider encountered some error.
    else:
        req_act = dict()
        for k, v in act_rest_answer['svm_vector'].iteritems():
            req_act[k] = float(v)
        activity = get_curr_activity(req_act)

    ''' Get id of all poi and rate them based on activity, context and distance. '''
    for key, val in poi_lst_of_dict.iteritems():
        f_res = lookup_table[part_of_day][activity][decode_category(val['fw_core']['category'])]
        s_res = grade_distance(coordinates['lat'], coordinates['lon'], val['fw_core']['location']['wgs84'][
            'latitude'], val['fw_core']['location']['wgs84']['longitude'])
        poi_dict[key] = f_res * s_res

    ''' Slice out ignored. '''
    if ignore != 'None' and ignore in poi_dict:
        save_ignored_for_current_user(user_id, ignore)

    ignored = get_ignored_for_current_user(user_id)
    for ig_poi in ignored:
        if ig_poi in poi_dict:
            del poi_dict[ig_poi]
        elif ig_poi[:18] == 'some-temporary-key':
            key = Keys.objects.filter(temp=ig_poi, time__gte=datetime.now()-timedelta(minutes=3))
            del poi_dict[key.real]

    ''' Sort pois based on grades and return first 15 elements. '''
    sort_poi_lst = sorted(poi_dict.items(), key=operator.itemgetter(1), reverse=True)
    ret_dict = {"POIS": [], "activity": decode_activity(activity)}
    if len(sort_poi_lst) > 5:
        n_it = 5
    else:
        n_it = len(sort_poi_lst)
    for num in range(0, n_it):

        ret_dict['POIS'].append({sort_poi_lst[num][0]: poi_lst_of_dict[sort_poi_lst[num][0]]})

    # Delete old keys
    keys = Keys.objects.filter(time__lt=(datetime.now()-timedelta(minutes=3)))
    keys.delete()

    # Wait until all threads finish the job.
    for thread in threads:
        thread.join()

    return ret_dict
