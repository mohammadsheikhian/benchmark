import asyncio
import time

import aiohttp

response_status = []


async def download_site(session, url):
    async with session.get(url[1]) as response:
        print("Read {0} from {1}".format(response.status, url[1]))
        print(url[0])


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = []
    for i in range(19):
        sites.append((i, 'https://alpha-cas.carrene.com/apiv1/version'))

    for i in range(20):
        sites.append((i * 2, 'https://alpha-maestro.carrene.com/apiv1/version'))

#    sites = [
#        "https://www.jython.org",
#        "http://olympus.realpython.org/dice",
#    ] * 40
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

