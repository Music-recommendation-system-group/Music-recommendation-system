import pandas as pd
import csv
import time
import requests,random,bs4  
import re 
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

os.chdir(r"G:\wangyiyun")
def get_data():
    page=[0,35,70,105,140,175]
    count = 1
    # url = 'https://music.163.com/discover/playlist/'
    for num in page:
        try:
            url ='https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='+str(num)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/8'
                            '4.0.522.40'
            }
            
            r = requests.get(url, headers=headers)
            # response.encoding='utf-8'
            bs = bs4.BeautifulSoup(r.text,'html.parser') 
            # print(bs)
            playlist=bs.find(class_='m-cvrlst f-cb')
            mus_1=playlist.find_all('li')
            for mus in mus_1:
                href=mus.find(class_='dec').find('a')
                href=href.get('href')
                href='https://music.163.com'+href       
                xinxi(href)
                n=num
                print(count,"%.2f%%"%(count/35),n/35+1)
                count+=1
                if count>35:
                    count=1


        except Exception as e:
            print(str(e))


def xinxi (href):

    try:
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('log-level=3')        
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(href)
        time.sleep(2)
        driver.switch_to.frame('g_iframe')
        soup=BeautifulSoup(driver.page_source, 'lxml')
        ti=soup.find(class_='f-ff2 f-brk').text
        text=soup.find(class_='m-table')
        music_list=text.find_all('tr')
        for df in music_list[1:]:
            name=df.find(class_='txt').find('b')['title'].replace('\xa0',' ')
            t=df.find(class_='u-dur').text
            do=df.find_all(class_='text')
            man=do[0].find('span')['title'].replace('\xa0',' ')
            book=do[1].find('a')['title'].replace('\xa0',' ')
            print(name,t,man,book,ti)
            datas.append([name,t,man,book,ti])
        driver.quit()
    except Exception as k :
        print(str(k))
        print(href)
        fail.append(href)
    
def xieru():
    with open('yes.csv',"w",encoding = 'gb18030',newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(['歌名','时间','歌手','专辑名字','歌单名称'])
            for e in datas:
                writer.writerows([e])
    
    with open('no.csv',"w",encoding = 'gb18030',newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(['网址'])
            for e in fail:
                writer.writerows([e])

if __name__ == '__main__':
    start = time.time()
    datas=[]
    fail=[]
    get_data()
    # xinxi()
    xieru()
    end = time.time()
    print('success')
    print(end-start)