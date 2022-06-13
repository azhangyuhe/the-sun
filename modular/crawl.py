import requests
import simplejson
import subprocess
from concurrent.futures import ThreadPoolExecutor
from config.auxiliary.encrypt import get_html, get_title


def get_response(page):
    try:
        if page['method'] == 'GET':
            try:
                response = requests.get(url=page['url'], headers=page['headers'], verify=False)
                if response.status_code == 404:
                    return ''
                headers = response.headers
                html = get_html(response)
                if html:
                    title = get_title(html)
                    return response.status_code, headers, title, html
                return ''
            except Exception:
                return ''
        else:
            try:
                response = requests.post(url=page['url'], headers=page['headers'], data=page['data'], verify=False)
                if response.status_code == 404:
                    return ''
                headers = response.headers
                html = get_html(response)
                if html:
                    title = get_title(html)
                    return response.status_code, headers, title, html
                return ''
            except Exception:
                return ''
    except Exception as error:
        print(error)


def scan(scanner):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3945.0 Safari/537.36", }
        target = f'{scanner.scheme}://{scanner.domain}'
        cmd = ["./thirdpart/crawlergo", "-c", "thirdpart/chrome-linux/chrome", "-t", "15", "-o", "json",
               "--ignore-url-keywords",
               "quit,exit,zhuxiao", "--custom-headers", simplejson.dumps(headers), target]
        rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = rsp.communicate()
        result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
        req_list = result["req_list"]
        tmp_list = []
        tmp_result = []
        for url_dic in req_list:
            if url_dic['url'] in tmp_list:
                continue
            tmp_list.append(url_dic['url'])
            tmp_result.append(dict(url_dic))
        scanner.website_page = tmp_result

        with ThreadPoolExecutor(max_workers=30) as pool:
            results = pool.map(get_response, scanner.website_page)
            num = 0
            for result in results:
                scanner.website_page[num]['response'] = result
                num += 1
    except Exception as error:
        print("crawl",error)
