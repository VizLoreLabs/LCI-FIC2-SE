import urllib2
import datetime
import json
import requests


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


def get_response_poi():
    headers = dict()
    headers['Content-type'] = 'application/json'
    poi = {"fw_core": {"location": {"wgs84": {"latitude": 45.001,
                                              "longitude": 19.001}},
                                   "category": 'kategorija',
                                   "name": {"": 'ime'},
                                   "short_name": {"": 'kratko_ime'},
                                   "label": {"": 'oznaka'},
                                   "source": "foursquare"
                               }
           }
    info = {"fw_core": {"location": {"wgs84": {"latitude": 45.011,
                                              "longitude": 19.011}},
                                   "category": 'kategorij',
                                   "name": {"": 'im'},
                                   "short_name": {"": 'kratko_im'},
                                   "label": {"": 'oznak'},
                                   "source": "foursquare"
                               }
           }
    response = requests.post('http://localhost/poi_dp/add_poi.php', data=json.dumps(info), headers=headers)
    obj = json.loads(response.text)
    print obj['created_poi']['uuid']
    print obj['created_poi']['timestamp']

get_response_poi()

