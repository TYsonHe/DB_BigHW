import json
import re
import requests
from bs4 import BeautifulSoup
import os
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from RegexpReplacer import RegexpReplacer


class CrawlManager():
    def __init__(self, name):
        self.name = name
        self.comments = []

    def setFileNames(self, JsonFileName, TxtFileName):
        self.JsonFileName = JsonFileName
        self.TxtFileName = TxtFileName

    def setTarget(self, targetUrl, start, limit):
        """
        设置爬取目标Url
        :param targetUrl: 目标Url
        :return: None
        """
        temp = targetUrl
        temp += '?start={}&limit={}&status=P&sort=new_score'.format(start, limit)
        self.targetUrl = temp
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

    def getHtml(self):
        """
        获取目标Url的Html
        :return: 目标Url的Html
        """
        try:
            self.html = requests.get(self.targetUrl, headers=self.headers)
        except Exception as e:
            print(f'爬取失败, ErrorMessage{e}')
        return None

    def PickInfo(self):
        """
        提取目标Url的Html中的信息
        :return: None
        """
        print('正在爬取数据，请稍后……')
        # 将一段文档传入BeautifulSoup的构造方法,就能得到一个文档的对象, 可以传入一段字符串
        soup = BeautifulSoup(self.html.text, 'lxml')
        target = soup.find_all('span', {'class': 'short'})
        for item in target:
            strs = item.get_text()
            self.comments.append(strs)
        return None

    def saveJsonFile(self):
        jsons = []
        id = 0
        for item in self.comments:
            id += 1
            item = re.sub(r"\"", "", item)
            jsons.append({"id": id, "comment": item})
        jsons = str(jsons)
        replacer = RegexpReplacer()
        jsons = replacer.replace(jsons)
        jsons = jsons.replace("\'", '\"')
        print(jsons)
        json_data = json.loads(jsons)

        with open('./FilmInfo/' + self.JsonFileName, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False)
        print('保存成功,文件名为' + self.JsonFileName)

    def getTextFromJson(self):
        with open('./FilmInfo/' + self.JsonFileName, 'r', encoding='utf-8') as file:
            self.comments = json.loads(file.read())
        self.JsonText = []
        for item in self.comments:
            self.JsonText.append(item['comment'])
        return None

    def clearSpecialChar(self):
        """
        清除特殊字符
        :return: None
        """
        self.content = []
        for item in self.JsonText:
            item = re.sub(r"\n|\t|\r|\r\n|\n\r|\x08|\\", "", item)
            self.content.append(item)
        return None

    def saveTxtFile(self):
        self.temp = ''
        for item in self.content:
            self.temp += item
        with open('./FilmInfo/' + self.TxtFileName, 'w', encoding='utf-8') as f:
            f.write(self.temp)
        self.temp = ''
        print('保存成功,文件名为' + self.TxtFileName)
        return None

    def getTextFromTxt(self):
        with open('./FilmInfo/' + self.TxtFileName, 'r', encoding='utf-8') as file:
            self.TxtText = file.read()
        return None

    def cutTxt(self):
        """
        对TxtText进行分词
        :return: None
        """
        self.cutText = jieba.cut(self.TxtText.strip())
        print('分词结果:')
        print(self.cutText)
        return None

    def moveStopWords(self):
        """
        去除停用词
        :return: None
        """
        self.stopwords = [line.strip() for line in open('./FilmInfo/stopwords.txt', encoding='UTF-8').readlines()]
        self.outText = ''
        for word in self.cutText:
            if word not in self.stopwords:
                if word != '\t':
                    self.outText += word
                    self.outText += ' '
        return None

    def drawCounts(self):
        """
        绘制词频统计图
        :return: None
        """
        self.words = jieba.lcut(self.outText)
        self.counts = {}
        for word in self.words:
            if len(word) == 1:
                continue
            else:
                self.counts[word] = self.counts.get(word, 0) + 1
        # 词频统计结果,按照词频从大到小排序
        self.counts = sorted(self.counts.items(), key=lambda x: x[1], reverse=True)
        for i in range(10):
            word, count = self.counts[i]
            # 输出前10个
            print("{0:<10}{1:>5}".format(word, count))

        # 绘制柱状图
        x_word = []
        y_count = []
        for i in range(10):
            word, count = self.counts[i]
            x_word.append(word)
            y_count.append(count)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.figure(figsize=(20, 15))
        plt.bar(range(len(y_count)), y_count, color='r', tick_label=x_word, facecolor='#9999ff', edgecolor='white')
        plt.xticks(rotation=45, fontsize=20)
        plt.yticks(fontsize=20)

        plt.title(self.name + '短评词频统计图', fontsize=24)
        plt.savefig('./FilmInfo/' + self.name + '短评词频统计图.jpg')
        # plt.show()
        return None

    def drawWordCloud(self):
        self.wc = WordCloud(font_path=r'.\static\fonts\simhei.ttf', width=800, height=600,
                            background_color=None).generate(self.outText)
        plt.imshow(self.wc, interpolation='bilinear')
        plt.axis('off')
        # plt.show()
        plt.savefig('./FilmInfo/' + self.name + '短评词云图.jpg')
        return None


if __name__ == "__main__":
    # 准备工作
    crawlManager = CrawlManager('《碟中谍6》')
    crawlManager.setFileNames('《碟中谍6》短评.json', '《碟中谍6》短评.txt')
    if os.path.exists('./FilmInfo/' + crawlManager.JsonFileName) == False:
        print('文件不存在，开始爬取页面。')
        limit = 10
        for i in range(10):
            crawlManager.setTarget('https://movie.douban.com/subject/26336252/comments', i * limit, limit)
            crawlManager.getHtml()
            crawlManager.PickInfo()
        crawlManager.saveJsonFile()
    else:
        crawlManager.getTextFromJson()
        crawlManager.clearSpecialChar()
        if os.path.exists('./FilmInfo/' + crawlManager.TxtFileName) == False:
            crawlManager.saveTxtFile()
        else:
            crawlManager.getTextFromTxt()
            crawlManager.cutTxt()
            crawlManager.moveStopWords()
            crawlManager.drawCounts()
            crawlManager.drawWordCloud()
