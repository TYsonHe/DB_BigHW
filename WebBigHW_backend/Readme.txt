python版本3.9.13

项目文件结构说明
BookInfo是存放爬取的书籍信息的文件夹
FilmInfo是存放爬取的电影信息的文件夹
static是存放静态文件的文件夹,包含fonts,images,js,css
templates是存放html文件的文件夹

.py文件说明
DataCollect.py, DataWash.py MakeWordCloud.py是爬取数据,清洗数据,制作词云的文件----初版，服务于爬取书籍信息
DataForFilms.py是爬取电影信息的文件 用类方式集成了爬取数据,清洗数据,制作词云的功能----改进，服务于爬取电影信息
但仍需自行将.csv文件导入数据库