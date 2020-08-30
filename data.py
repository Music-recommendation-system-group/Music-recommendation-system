from urllib import parse
from lxml import etree
from urllib3 import disable_warnings
import requests
import csv


class Wangyiyun(object):

    def __init__(self, **kwargs):
        # 歌单风格
        self.types = kwargs['types']
        # 歌单类型
        self.years = kwargs['years']
        # 爬取十页
        self.pages = pages
        # 页数
        self.limit = 35
        self.offset = 35 * self.pages - self.limit
        # url
        self.url = "https://music.163.com/discover/playlist/?"

    # 设置请求头部信息
    def set_header(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1',
        }
        return self.header

    # 设置请求表格信息
    def set_froms(self):
        self.key = parse.quote(self.types)
        self.froms = {
            "cat": self.key,
            "order": self.years,
            "limit": self.limit,
            "offset": self.offset,
        }
        return self.froms

    # 解析代码，获取有用的数据
    def parsing_codes(self):
        page = etree.HTML(self.code)
        # 标题
        self.title = page.xpath('//div[@class="u-cover u-cover-1"]/a[@title]/@title')
        # 作者
        self.author = page.xpath('//p/a[@class="nm nm-icn f-thide s-fc3"]/text()')
        # 阅读量
        self.listen = page.xpath('//span[@class="nb"]/text()')
        # 歌单链接
        self.link = page.xpath('//div[@class="u-cover u-cover-1"]/a[@href]/@href')
        # 将数据保存为csv文件
        data = list(zip(self.title, self.author, self.listen, self.link))
        with open('yinyue.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # writer.writerow(header)
            writer.writerows(data)

    # 获取网页源代码
    def get_code(self):
        disable_warnings()
        self.froms['cat'] = self.types
        disable_warnings()
        self.new_url = self.url + parse.urlencode(self.froms)
        self.code = requests.get(
            url=self.new_url,
            headers=self.header,
            data=self.froms,
            verify=False,
        ).text

    # 爬取多页时刷新offset
    def multi(self, page):
        self.offset = self.limit * page - self.limit


if __name__ == '__main__':
    # 歌单的歌曲风格
    types = "说唱"
    # 歌单的发布类型:最热=hot，最新=new
    years = "hot"
    # 指定爬取的页数
    pages = 10
    # 通过pages变量爬取指定页面
    music = Wangyiyun(
        types=types,
        years=years,
    )
    for i in range(pages):
        page = i + 1  # 因为没有第0页
        music.multi(page)  # 爬取多页时指定，传入当前页数，刷新offset
        music.set_header()  # 调用头部方法，构造请求头信息
        music.set_froms()  # 调用froms方法，构造froms信息
        music.get_code()  # 获取当前页面的源码
        music.parsing_codes()  # 处理源码，获取指定数据

import pandas as pd

# 读取文件
data = pd.read_csv(r"yinyue.csv", encoding="utf-8")
data.columns = ('title', 'author', 'listen_num', 'link')
data

# 删除没有万单位的行
data = data[data["listen_num"].str[-1] == "万"]
data

# 删除万单位
data['listen_num'] = data['listen_num'].str.strip("万").apply(int)
data

# 删除重复值
data = data.drop_duplicates()
data.head()

data.describe()

# 按播放数量进行降序排序
data = data.sort_values('listen_num', ascending=False).head(10)
data

