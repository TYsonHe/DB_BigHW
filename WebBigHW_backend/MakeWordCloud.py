import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='crawler_data',
    charset='utf8'
)

cur = conn.cursor()
sql = "select comment from books"
data = cur.execute(sql)
result = cur.fetchall()
text = ''
for item in result:
    text = text + item[0]
cur.close()
conn.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)
print(string)


img = Image.open(r'.\static\img\tree.jpg')
img_array = np.array(img)
wc = WordCloud(
    font_path=r'.\static\fonts\msyh.ttc',
    mask=img_array,
    background_color='white',
)
wc.generate_from_text(string)
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
plt.show()

wc.to_file(r'.\static\img\wordcloud_books.jpg')
