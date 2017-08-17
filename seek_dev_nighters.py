from datetime import datetime
import requests
import json
import pytz

API_LINK = 'http://devman.org/api/challenges/solution_attempts/'


def get_api_pages_quantity():
    return json.loads(requests.get(API_LINK).text)['number_of_pages']


def load_attempts():
    load_attempts_pages_num = get_api_pages_quantity()
    load_attempts_common_list = []

    for page in range(1, load_attempts_pages_num + 1):
        reply_text = requests.get(API_LINK, params={'page': page}).text
        records_on_page = json.loads(reply_text)['records']
        for record in records_on_page:
            load_attempts_common_list.append(record)

    return load_attempts_common_list


def get_midnighters(load_attempts_common_list):
    midnighters_list = []
    for load_attempt in load_attempts_common_list:
        if load_attempt['timestamp']:
            local_datetime = (pytz.timezone(load_attempt['timezone'])
                              .localize(datetime.fromtimestamp(load_attempt['timestamp'])))
            if local_datetime.hour in range(6):
                midnighters_list.append({'username': load_attempt['username'],
                                         'load_attempt_time': local_datetime.strftime('%H:%m')})

    return midnighters_list

if __name__ == '__main__':
    load_attempts_list = load_attempts()

    for midnighter in get_midnighters(load_attempts_list):
        print('{} sent a solution at {}'.format(midnighter['username'], midnighter['load_attempt_time']))
