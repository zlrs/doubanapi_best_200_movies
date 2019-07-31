import json
import requests
import time
start_time = time.perf_counter()
max_num = 20

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
    print("正在爬取第{}-{}部电影:".format(start, start+20))
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

print("done!")

end_time = time.perf_counter()
with open("perf.txt", "w", encoding='utf-8') as f:
    alert = f'Blocking version spider uses {end_time - start_time}s to {max_num} movies.'
    f.write(alert)
    print(alert)
