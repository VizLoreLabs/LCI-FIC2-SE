__author__ = 'luigi'
import urllib2
import datetime
import json


def test_recommend():
    url = 'http://localhost:8433/recommend/'
    headers = dict()
    headers['Content-type'] = 'application/json'
    data = "'uuid': 'an32524fadfkl09jk1', 'lat': 12.458935, 'lng': 24.553212"
    request = urllib2.Request(url, data, headers)
    result = urllib2.urlopen(request).read()
    print result


def get_time():
    ms = 1424973621
    time = datetime.datetime.fromtimestamp(ms)
    print time.hour


def get_activity():
    url = 'http://130.211.136.203:8080/ac/?ac=1&uuid=adadd2df02dc2e5e&alg=svm&fs=standard&tp=3600'
    headers = dict()
    headers['Accept'] = 'application/json'
    result = None
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        if e.code == 404 or e.code == 500:
            return 'None'
    return result


def get_poi(lat, lon, radius):
    url = 'http://130.211.136.203/poi_dp/radial_search.php?lat=%f&lon=%f&radius=%d' % (lat, lon, radius)
    headers = dict()
    headers['Content-type'] = 'application/json'
    result = None
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request).read()
    except urllib2.HTTPError:
        print "error"
        return None
    return result

print get_poi(41.4022365, 2.1887515, 500)