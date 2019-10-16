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
count_of_requests = 100
count_of_threads = 5
analyze_thread = {}


class StatusAnalize:
    success_status = 0
    failed_status = 0


def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
        analyze_thread[threading.get_ident()] = StatusAnalize()
    return thread_local.session


def call_APIs(url):
    start_times[url[0]] = perf_counter()
    session = get_session()
    with session.request('VERIFY',url[1]) as response:
        end_times[url[0]] = perf_counter()
        request_threads[url[0]] = (threading.get_ident(), response.status_code)


def call_all_APIs(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=count_of_threads) as executor:
        executor.map(call_APIs, sites)


def analyze_status_code(request_threads):
    for request in request_threads:
        if 500 <= request_threads[request][1] < 600:
            analyze_thread[request_threads[request][0]].failed_status += 1
        else:
            analyze_thread[request_threads[request][0]].success_status += 1

    for thread_identity in analyze_thread:
        print(f'Thread identyti: {thread_identity}')
        print(
            f'Success requests: {analyze_thread[thread_identity].success_status}'
        )
        print(
            f'Failed requests: {analyze_thread[thread_identity].failed_status}\n'
        )


def analyze_time():
    for i in range(count_of_requests):
        duration_times[i] = end_times[i]-start_times[i]

    list_of_duration_times = [v for v in duration_times.values()]
    list_of_duration_times.sort()
#    print(f'All times: {list_of_duration_times}')

    min_duration_time = list_of_duration_times[0]
    print(f'Minimum time: {min_duration_time}')

    max_duration_time = list_of_duration_times[-1]
    print(f'Maximum time: {max_duration_time}')

    mean_duration_time = sum(list_of_duration_times) / count_of_requests
    print(f'mean time: {mean_duration_time}\n')


if __name__ == '__main__':
    APIs = []
    for i in range(count_of_requests):
        APIs.append((i, 'http://alpha-cas.carrene.com/apiv1/version'))

    start_time = time.time()
    call_all_APIs(APIs)
    duration = time.time() - start_time
    print(f'Downloaded {len(APIs)} in {duration} seconds\n')

    analyze_time()
    analyze_status_code(request_threads)

