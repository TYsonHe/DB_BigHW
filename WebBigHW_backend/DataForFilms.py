import requests
from lxml import etree
import os
import pandas as pd
import re
import jieba
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud


class DataForFilms:
    def __init__(self):
        self.films = []
        self.imgUrls = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    def setUrl(self, url):
        self.url = url

    def getHtml(self):
        """
        获取网页源代码
        存储到self.htmlText
        :return: None
        """
        try:
            self.html = requests.get(self.url, headers=self.headers)
            self.html.encoding = self.html.apparent_encoding
            if self.html.status_code == 200:
                print('成功获取源代码')
            self.htmlText = self.html.text
        except Exception as e:
            print('获取源代码失败：%s' % e)
        return None

    def praseHtml(self):
        """
        解析网页源代码
        存储到self.films和self.imgUrls
        :return: None
        """
        self.html = etree.HTML(self.htmlText)
        li = self.html.xpath("//ol[@class='grid_view']//li")
        print(len(li))
        for t in li:
            chineseTitle = t.xpath(".//div[@class='item']//div[@class='info']//a//span[1]/text()")[0]
            otherTitle = t.xpath(".//div[@class='item']//div[@class='info']//a//span[2]/text()")[0]
            otherTitle=otherTitle.split(r'/')[1].strip()
            print(otherTitle)
            #print(Title)
            link = t.xpath(".//div[@class='item']//div[@class='info']//a/@href")[0]
            #print(link)
            p1=t.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//p[1]")[0].xpath('string()')
            p1=p1.strip().replace('\n','+').replace(' ','')
            p1=p1.replace(u'\xa0','')
            #print(p1)
            director=p1.split('导演:')[1].split('主')[0]
            #print(director)
            if "主演:" not in p1:
                actor='无'
            else:
                actor=p1.split('主演:')[1].split('/')[0].split('...')[0]
            #print(actor)

            year=p1.split('+')[1].split('/')[0]
            #print(year)
            country=p1.split('+')[1].split('/')[1]
            #print(country)
            type=p1.split('+')[1].split('/')[2]
            #print(type)
            score=t.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//div[@class='star']//span[@class='rating_num']/text()")[0]
            #print(score)
            star=int(float(score))/2
            #print(star)
            pnum=t.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//div[@class='star']//span[4]/text()")[0]
            pnum=re.findall(r'\d+',pnum)[0]
            #print(pnum)

            comments=t.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//p[@class='quote']/span/text()")
            comment=comments[0] if len(comments)!=0 else '无'
            #print(comment)
            #print([Title,link,director,actor,year,country,type,score,star,pnum,comment])
            film={
                '电影名字':chineseTitle,
                '别名':otherTitle,
                '电影链接':link,
                '导演':director,
                '主演':actor,
                '年份':year,
                '国家':country,
                '类型':type,
                '评分':score,
                '星级':star,
                '评价人数':pnum,
                '评论':comment
            }
            self.films.append(film)

            #图片
            imgUrl=t.xpath(".//div[@class='item']//div[@class='pic']//img/@src")[0]
            #print(imgUrl)
            self.imgUrls.append(imgUrl)
            
        return None

    def downloadImg(self,film,imgUrl):
        if 'FilmsImg' in os.listdir(r'D:\大学\大二下\Web技术\WebBigHW_backend\FilmInfo'):
            pass
        else:
            os.mkdir(r'D:\大学\大二下\Web技术\WebBigHW_backend\FilmInfo\FilmsImg')
        os.chdir(r'D:\大学\大二下\Web技术\WebBigHW_backend\FilmInfo\FilmsImg')

        img=requests.request('get',imgUrl).content

        with open(film['电影名字']+'.jpg','wb') as f:
            f.write(img)

    def saveDataToCsv(self):
        filmData = pd.DataFrame(self.films)
        filmData.to_csv(r'D:\大学\大二下\Web技术\WebBigHW_backend\FilmInfo\FilmsData.csv', encoding='utf-8-sig', index=False)
        print('成功保存电影数据到csv文件')
        return None

    def dataWash(self):
        """
        数据清洗
        这里暂时没发现脏数据
        :return: None
        """
        pass

    def makeWordCloud(self,ImgSrc):
        text=''
        for i in range(len(self.films)):
            text+=self.films[i]['评论']
        cut=jieba.cut(text)
        cut_text=' '.join(cut)
        #print(cut_text)
        img=Image.open(ImgSrc)
        img_array=np.array(img)
        wc=WordCloud(
            background_color='white',
            mask=img_array,
            font_path='simhei.ttf'
        )
        wc.generate_from_text(cut_text)
        fig=plt.figure(1)
        plt.imshow(wc)
        plt.axis('off')
        #plt.show()
        wc.to_file(r'.\static\img\wordcloud_films.jpg')




if __name__ == '__main__':
    df = DataForFilms()
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}'.format(i * 25)
        df.setUrl(url)
        df.getHtml()
        df.praseHtml()
    # for i in range(250):
    #     df.downloadImg(df.films[i],df.imgUrls[i])
    df.saveDataToCsv()
    # 加上想要的背景结构图
    df.makeWordCloud(r'.\static\img\tree.jpg')