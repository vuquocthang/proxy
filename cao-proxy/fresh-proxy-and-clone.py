import chilkat
import requests
from queue import Queue
import threading
import sys
import random
import logging
logging.basicConfig(filename='fresh-proxy.log',level=logging.DEBUG)

logging.info("Begin fresh")

url = "http://toolnuoi999.tk/api"
threads = 5
proxies = requests.get("{}/proxies".format(url)).json()

q = Queue()

def _create_workers():
    for x in range(threads):
        t = threading.Thread(target=_work)
        t.daemon = True
        t.start()

def _work():
    while True:
        proxy = q.get()
        _job(proxy)
        q.task_done()

def _job(proxy):
    try:
        _check(proxy)
    except Exception as e:
        print(e)

def _check(proxy):
    try:
        r = requests.get("https://api.ipify.org/?format=json", proxies={
            'https' : '{}:{}'.format(proxy['ip'].strip(), proxy['port'].strip())
        }).json()

        if r['ip'].strip() == proxy['ip'].strip():
            update_proxy(proxy, 1)
            return True
        else:
            update_proxy(proxy, 0)
            return False
    except Exception as e:
        print(e)
        update_proxy(proxy, 0)
        return False


def update_proxy(proxy, status):
    print('update proxy : {} with status : {}'.format(proxy, status))

    requests.put("{}/proxy/{}".format(url, proxy['id']), {
        'status': status
    })

_create_workers()
for proxy in proxies:
    q.put(proxy)
q.join()
