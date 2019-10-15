import concurrent.futures
import threading
import time
from time import perf_counter

import requests


thread_local = threading.local()


start_times = dict()
end_times = dict()
l = dict()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    start_times[url[0]] = perf_counter()
    session = get_session()
#    l[threading.current_thread().ident] = 'asd'
    l[threading.get_ident()] = 'asd'
    with session.get(url[1]) as response:
        end_times[url[0]] = perf_counter()


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = []
    for i in range(50):
        sites.append((i, 'http://0.0.0.0:8083/apiv1/version'))

#    for i in range(2):
#        sites.append((i * 2, 'https://alpha-maestro.carrene.com/apiv1/version'))
#
#
#    sites = [
#        "https://www.jython.org",
#        "http://olympus.realpython.org/dice",
#    ] * 40
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
#    print('Start\n')
#    print(start_times)
#    print('\nEndi\n')
    print(end_times)

    for i in range(50):
        print(end_times[i]-start_times[i])

    print(l)
