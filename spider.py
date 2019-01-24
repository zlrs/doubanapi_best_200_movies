import json
import requests

# content: 列表，用于存放200条电影数据
content = []
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/tag/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

# 爬取
for start in range(0, 200, 20):
    print("正在爬取第{}-{}部电影:".format(start, start+20))
    # 构造url. sort=S: 按评分排序。
    url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=&start={}&year_range=2018,2018'.format(start)
    r = requests.get(url, headers=headers)
    json_obj = json.loads(r.text)
    movie_list = json_obj['data']
    for i, movie in enumerate(movie_list):
        content.append({
            "title": movie['title'],
            "rate": movie['rate'],
            "cover": movie['cover']
        })
    # 循环末端可以适当延时一段时间

# dump to /ans.json
to_dump = {
    "data": content,
}
with open("ans.json", "w", encoding='utf-8') as f:
    json.dump(to_dump, f, ensure_ascii=False, indent=4)

print("done!")
