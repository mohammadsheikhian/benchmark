import concurrent.futures
import threading
import time
from time import perf_counter

import requests


thread_local = threading.local()
start_times = dict()
end_times = dict()
duration_times = dict()
request_threads = dict()
list_of_duration_times = []
min_duration_time = 0
max_duration_time = 0
mean_duration_time = 0
count_of_requests = 1000
count_of_threads = 10


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    start_times[url[0]] = perf_counter()
    session = get_session()
    with session.request('VERIFY',url[1]) as response:
        end_times[url[0]] = perf_counter()
        request_threads[url[0]] = (threading.get_ident(), response.status_code)


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=count_of_threads) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = []
    for i in range(count_of_requests):
        sites.append((i, 'http://192.168.1.80/apiv1/tokens/86/codes/924F0A6214F59712?primitive=yes'))

    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")

    for i in range(count_of_requests):
        duration_times[i] = end_times[i]-start_times[i]

    list_of_duration_times = [v for v in duration_times.values()]
    list_of_duration_times.sort()
    min_duration_time = list_of_duration_times[0]
    max_duration_time = list_of_duration_times[-1]
    #print(request_threads)
