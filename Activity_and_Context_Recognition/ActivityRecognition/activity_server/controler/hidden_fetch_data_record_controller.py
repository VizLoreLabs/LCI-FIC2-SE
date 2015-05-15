import numpy as np
from activity_server.models import DataRecord, activity_table, activity_table_json
from datetime import datetime, timedelta


def recognize_last_activities(uuid, algorithm, feature_set, start_ts, end_ts):

    start_datetime = datetime.fromtimestamp(start_ts / 1e3)
    end_datetime = datetime.fromtimestamp(end_ts / 1e3)

    records = DataRecord.objects.filter(user_id=uuid)\
        .filter(date_time__gt=start_datetime)\
        .filter(date_time__lt=end_datetime)

    if records:
        avg_prob = [0, 0, 0, 0, 0, 0, 0, 0]

        current_activity = "none"

        for j in xrange(len(records)):
            prob = get_probability_for_data_record(records[j], feature_set, algorithm)

            if j == 0:
                current_activity = activity_table_json.get(np.argmax(prob) + 1)

            for i in xrange(len(prob)):
                avg_prob[i] += prob[i]/len(records)

        return {"vector": avg_prob, "time": records[0].date_time, "current_activity": current_activity}
    else:
        raise Exception('No record found')


def get_probability_for_data_record(record, feature_set, algorithm):
    if algorithm == 'svm' and feature_set == 'standard':
        return record.activity.svm
    elif algorithm == 'svm' and feature_set == 'enhanced':
        return record.activity.svm_ech
    elif algorithm == 'dt' and feature_set == 'standard':
        return record.activity.dt
    elif algorithm == 'dt' and feature_set == 'enhanced':
        return record.activity.dt_ech
    else:
        raise Exception("Bad request")