import json
import urllib.request


def send_to_slack(url, message):
    data = {
        'text': message,
    }
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except urllib.error.HTTPError as err:
        pass
    except urllib.error.URLError as err:
        pass
    return body

def send_to_teams(url, message):
    data = {
        'text': message,
    }
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except urllib.error.HTTPError as err:
        return
    except urllib.error.URLError as err:
        return
    return body