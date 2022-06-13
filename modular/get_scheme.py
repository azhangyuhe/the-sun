import requests
from urllib3.exceptions import InsecureRequestWarning


def scan(scanner):
    try:
        http_response = requests.get(url=f'http://{scanner.domain}', headers=scanner.headers, allow_redirects=False)
        if http_response.status_code == 200:
            scanner.scheme = 'http'
            return True
    except (requests.exceptions.ConnectionError, Exception) as error:
        pass
    try:
        https_response = requests.get(url=f'https://{scanner.domain}', headers=scanner.headers, verify=False)
        if https_response.status_code == 200:
            scanner.scheme = 'https'
            return True
    except (InsecureRequestWarning, requests.exceptions.SSLError, Exception) as error:
        pass

    return False
