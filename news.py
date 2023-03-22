import requests
import time
import re
from lxml import etree
# from wxauto import *
import os

token = os.environ['MY_TOKEN']
session = requests.session()

url = 'https://www.cls.cn/api/sw?app=CailianpressWeb&os=web&sv=7.7.5&sign=bf0f367462d8cd70917ba5eab3853bce'


def main():
    data = {
        'app': "CailianpressWeb",
        'keyword': "你需要知道的隔夜全球要闻",
        'os': "web",
        'sv': "7.7.5",
        'type': "all"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', }
    response = session.post(url=url, json=data, headers=headers)
    response = response.json()
    news = response['data']['telegram']['data'][0]['descr']
    timeStamp = response['data']['telegram']['data'][0]['time']
    timeArray = time.localtime(timeStamp)
    formatTime = time.strftime("%Y年%m月%d日", timeArray)
    news = re.sub(r'(\d+、)', r'\n\1', news)
    formatNews = ''.join(etree.HTML(news).xpath('//text()'))
    title = formatNews.split('\n', 1)[0]
    news = formatNews.split('\n', 1)[1]
    param = {"title": f"{formatTime} {title}",
             "content": f"{news}",
             "template": "html",
             "token": token,
             }
    requests.post(url="https://www.pushplus.plus/send", headers=headers, data=param)


if __name__ == '__main__':
    main()
