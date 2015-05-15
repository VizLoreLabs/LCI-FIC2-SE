import numpy as np
from activity_server.models import DataRecord, activity_table, activity_table_json
from datetime import datetime, timedelta


def recognize_last_activity(uuid, algorithm, feature_set):

    record = DataRecord.objects.raw_query({'user_id': {'$eq': uuid}}).reverse()[:1]

    if algorithm == 'svm' and feature_set == 'standard':
        prob = record[0].activity.svm
    elif algorithm == 'svm' and feature_set == 'enhanced':
        prob = record[0].activity.svm_ech
    elif algorithm == 'dt' and feature_set == 'standard':
        prob = record[0].activity.dt
    elif algorithm == 'dt' and feature_set == 'enhanced':
        prob = record[0].activity.dt_ech
    else:
        raise Exception("Bad request")

    current_activity = activity_table_json.get(np.argmax(prob) + 1)

    return {"vector": prob, "time": record[0].date_time, "current_activity": current_activity}


def recognize_last_activities(uuid, algorithm, feature_set, delta_time):

    datetime_point = datetime.now() - timedelta(seconds=delta_time)
    records = DataRecord.objects.filter(user_id=uuid).filter(date_time__gt=datetime_point)

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