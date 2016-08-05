from ratelimiter import RateLimiter
import datetime
import os
import json

import requests


API_KEY = '174-bb96326ac744ca6ca3161cc6778cff85'

HELLO_ENDPOINT = 'http://2016sv.icfpcontest.org/api/hello'
LIST_ENDPOINT = 'http://2016sv.icfpcontest.org/api/snapshot/list'
BLOB_ENDPOINT = 'http://2016sv.icfpcontest.org/api/blob/{}'

hour_limiter = RateLimiter(max_calls=1000, period=60*60)
second_limiter = RateLimiter(max_calls=1, period=1.1)

def api_session():
    with hour_limiter:
        with second_limiter:
            session = requests.Session()
            session.headers.update({'X-API-Key': API_KEY})
            return session


def check_status(resp):
    if resp.status_code >= 500 and resp.status_code < 600:
        raise TransientError()
    if resp.status_code != 200:
        raise PermanentError(resp)

class TransientError(Exception):
    pass

class PermanentError(Exception):
    def __init__(self, resp):
        Exception.__init__(self)
        self.resp = resp
    def __str__(self):
        return 'Error, http status: {}, resp: {}'.format(self.resp.status_code, self.resp.text)

def api_retry(fn):
    def decorator(*args, **kwargs):
        retries = 3
        while retries > 0:
            try:
                return fn(*args, **kwargs)
            except TransientError:
                retries -= 1

    return decorator

def get_hello():
    return api_session().get(HELLO_ENDPOINT).json()

@api_retry
def latest_snapshot():
    resp = api_session().get(LIST_ENDPOINT)
    check_status(resp)
    return resp.json()['snapshots'][-1]

@api_retry
def fetch_blob(ref):
    resp = api_session().get(BLOB_ENDPOINT.format(ref))
    check_status(resp)
    return resp.text

def fetch_problems(workdir):
    snapshot_ref = latest_snapshot()
    datetime_label = datetime.datetime.utcfromtimestamp(snapshot_ref['snapshot_time'])
    snapshot_name = os.path.join(workdir, 'snapshot_{}_{}.json'.format(datetime_label, snapshot_ref['snapshot_hash']))
    snapshot = fetch_blob(snapshot_ref['snapshot_hash'])
    with open(snapshot_name, 'w') as f:
        f.write(snapshot)
    for p in json.loads(snapshot)['problems']:
        problem_name = os.path.join(workdir, 'problem_{problem_id:04}_{problem_size}.json'.format(**p))
        p['spec'] = fetch_blob(p['problem_spec_hash'])
        print 'Problem: {}'.format(problem_name)
        with open(problem_name, 'w') as f:
            f.write(json.dumps(p))



if __name__ == '__main__':
    workdir = 'problems'
    os.mkdir(workdir)
    fetch_problems(workdir)
