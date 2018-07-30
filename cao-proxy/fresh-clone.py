#import chilkat
import requests
from queue import Queue
import threading
import sys
import random
import logging
logging.basicConfig(filename=os.path.abspath('fresh-clone.log'),level=logging.DEBUG)

logging.info("===============> Begin fresh clone")

url = "http://toolnuoi999.tk/api"
threads = 5
clones = requests.get("{}/clones".format(url)).json()

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

def _job(clone):
    try:
        _check(clone)
    except Exception as e:
        print(e)

def _check(clone):
    try:
        r = requests.get("https://api.ipify.org/?format=json", proxies={
            'https' : '{}:{}'.format(clone['ip'].strip(), clone['port'].strip())
        }).json()

        if r['ip'].strip() == clone['ip'].strip():
            return True
        else:
            proxy = requests.get("{}/proxy".format(url)).json()

            update_clone(clone, proxy['ip'].strip(), proxy['port'].strip())
            return False
    except Exception as e:
        print(e)
        proxy = requests.get("{}/proxy".format(url)).json()
        update_clone(clone, proxy['ip'].strip(), proxy['port'].strip())
        return False


def update_clone(clone, ip, port):
    print("update clone : {}".format(clone['id']))

    requests.put("{}/clone/{}".format(url, clone['id']), {
        'ip': ip,
        'port': port
    })

_create_workers()

for clone in clones:
    q.put(clone)
q.join()
