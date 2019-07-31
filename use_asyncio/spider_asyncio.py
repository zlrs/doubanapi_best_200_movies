import asyncio
import aiohttp
import json
from typing import Tuple
import time

user_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/tag/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
api_endpoint = 'https://movie.douban.com/j/new_search_subjects'
api_params = dict(
    sort='S',
    range='0,10',
    tags='',
    start=None,  # Int
    year_range='2018,2018'
)
content = []


async def fetch(session, base_url, params, headers):
    async with session.get(base_url, params=params, headers=headers) as response:
        json_obj = await response.json()
        movie_list = json_obj['data']
        for i, movie in enumerate(movie_list):
            content.append({
                "title": movie['title'],
                "rate": movie['rate'],
                "cover": movie['cover']
            })


async def main(max_num: int):
    async with aiohttp.ClientSession() as session:
        for start in range(0, max_num, 20):
            api_params['start'] = start
            tasks = fetch(session, api_endpoint, api_params, user_headers)
        await asyncio.gather(tasks)

    # dump to /ans.json
    to_dump = {
        "data": content,
    }
    with open("ans_asyncio.json", "w", encoding='utf-8') as f:
        json.dump(to_dump, f, ensure_ascii=False, indent=4)

    print("done!")

start_time = time.perf_counter()
max_num = 20
asyncio.run(main(max_num))
end_time = time.perf_counter()
with open("perf.txt", "w", encoding='utf-8') as f:
    alert = f'Asyncio version spider uses {end_time - start_time}s to {max_num} movies.'
    f.write(alert)
    print(alert)
