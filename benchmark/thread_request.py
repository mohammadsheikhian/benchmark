import concurrent.futures
import threading
import time
from time import perf_counter

import requests

from benchmark.helpers import StatusAnalize, Request

thread_local = threading.local()
start_times = dict()
end_times = dict()
duration_times = dict()
request_threads = dict()
list_of_duration_times = []
min_duration_time = None
max_duration_time = None
mean_duration_time = None
COUNT_OF_REQUESTS = None
COUNT_OF_THREADS = None
analyze_thread = {}


def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
        analyze_thread[threading.get_ident()] = StatusAnalize()
    return thread_local.session


def call_APIs(site):
    start_times[site.index] = perf_counter()
    session = get_session()
    with session.request(
        site.method_name,
        site.url,
        data=site.form,
        headers=site.headers
    ) as response:
        end_times[site.index] = perf_counter()
        request_threads[site.index] = (
            threading.get_ident(),
            response.status_code
        )


def call_all_APIs(sites):
    global COUNT_OF_THREADS
    with concurrent.futures.ThreadPoolExecutor(max_workers=COUNT_OF_THREADS) \
        as executor:
        executor.map(call_APIs, sites)


def analyze_status_code(request_threads):
    for request in request_threads:
        if 500 <= request_threads[request][1] < 600:
            analyze_thread[request_threads[request][0]].failed_status += 1
        else:
            analyze_thread[request_threads[request][0]].success_status += 1

    for thread_identity in analyze_thread:
        print(f'Thread identity: {thread_identity}')
        print(
            f'Success requests: {analyze_thread[thread_identity].success_status}'
        )
        print(
            f'Failed requests: {analyze_thread[thread_identity].failed_status}\n'
        )


def analyze_time():
    for i in range(COUNT_OF_REQUESTS):
        duration_times[i] = end_times[i]-start_times[i]

    list_of_duration_times = [v for v in duration_times.values()]
    list_of_duration_times.sort()

    min_duration_time = list_of_duration_times[0]
    print(f'Minimum time: {min_duration_time}')

    max_duration_time = list_of_duration_times[-1]
    print(f'Maximum time: {max_duration_time}')

    mean_duration_time = sum(list_of_duration_times) / COUNT_OF_REQUESTS
    print(f'mean time: {mean_duration_time}\n')


def run(count_of_requests, count_of_threads, url, method_name, form, headers):
    global COUNT_OF_REQUESTS
    COUNT_OF_REQUESTS = count_of_requests
    global  COUNT_OF_THREADS
    COUNT_OF_THREADS = count_of_threads

    request_APIs = []
    for i in range(count_of_requests):
        request_APIs.append(Request(
            index=i,
            url=url,
            method_name=method_name,
            form=form,
            headers=headers
       ))

    start_time = time.time()
    call_all_APIs(request_APIs)
    duration = time.time() - start_time
    print(f'Downloaded {len(request_APIs)} in {duration} seconds\n')

    analyze_time()
    analyze_status_code(request_threads)


if __name__ == '__main__':
    run()


