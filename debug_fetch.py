import urllib.request
from urllib.error import HTTPError
paths = ['/login/student/','/login/admin/']
for path in paths:
    url = 'http://127.0.0.1:8000' + path
    try:
        r = urllib.request.urlopen(url)
        data = r.read()
        print(f"{url} -> {r.getcode()} len={len(data)}")
    except HTTPError as e:
        print(f"{url} -> HTTPError {e.code}")
        try:
            body = e.read().decode('utf-8')
            print('BODY SNIPPET:\n', body[:2000])
        except Exception as ex:
            print('Failed to read error body:', ex)
    except Exception as ex:
        print(f"{url} -> ERROR {ex}")
