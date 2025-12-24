# 豆瓣电影 Top 250 光影画廊 (Douban Movie Gallery)

这是一个 Python 爬虫与数据可视化项目。

## ✨ 项目功能
1. **数据抓取**：自动爬取豆瓣 Top250 电影的详细信息（包括评分、导演、海报链接、热评等）。
2. **海报下载**：自动将海报图片下载到本地。
3. **可视化展示**：生成一个交互式的 HTML 海报墙网页，支持点击跳转豆瓣详情。

## 📂 文件结构
* `douban_main.py`: 爬虫脚本，负责抓取数据和下载图片。
* `create_gallery.py`: 可视化脚本，负责生成 HTML 网页。
* `douban_top250.json`: 爬取到的数据文件。
* `movie_gallery.html`: 最终生成的网页。
* `posters/`: 存放海报图片的文件夹。

## 🚀 如何使用
1. 运行 `douban_main.py` 抓取数据（可选，已有数据）。
2. 运行 `create_gallery.py` 生成网页。
3. 双击打开 `movie_gallery.html` 浏览。

## 📝 作者
skysstst