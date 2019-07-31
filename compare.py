from use_asyncio import spider_asyncio
from use_blocking_io import spider

for max_num in (20, 200, 2000):
    duration = spider.export(max_num)
    duration_asyncio = spider_asyncio.export(max_num)

    print(f'Blocking IO version spider takes {duration}s to fetch {max_num} movies.')
    print(f'Asyncio version spider takes {duration_asyncio}s to fetch {max_num} movies.')
