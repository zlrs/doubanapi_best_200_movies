import json
import requests
import time
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(message)s',
    filename='blocking_io.log',
)
logger = logging.getLogger(__name__)


def pLog(s):
    print(s)
    logger.info(s)


def export(max_num):
    start_time = time.perf_counter()

    # content: 列表，用于存放200条电影数据
    content = []
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/tag/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    # 爬取
    session = requests.sessions.Session()
    for start in range(0, max_num, 20):
        pLog("正在爬取第{}-{}部电影".format(start, start+20))
        # 构造url. sort=S: 按评分排序。
        url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=&start={}&year_range=2018,2018'.format(start)
        r = session.get(url, headers=headers)
        json_obj = json.loads(r.text)
        movie_list = json_obj['data']
        for i, movie in enumerate(movie_list):
            content.append({
                "title": movie['title'],
                "rate": movie['rate'],
                "cover": movie['cover']
            })

    session.close()
    # dump to /ans.json
    to_dump = {
        "data": content,
    }
    with open("ans.json", "w", encoding='utf-8') as f:
        json.dump(to_dump, f, ensure_ascii=False, indent=4)

    pLog("done!")

    end_time = time.perf_counter()
    with open("perf.txt", "a", encoding='utf-8') as f:
        alert = f'Blocking version spider takes {end_time - start_time}s to fetch {max_num} movies.'
        f.write(alert)
        pLog(alert)

    return end_time - start_time


if __name__ == '__main__':
    export(20)
