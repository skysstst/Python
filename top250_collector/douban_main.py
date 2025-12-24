# 豆瓣电影Top250爬虫

import requests
from bs4 import BeautifulSoup
import time
import csv
import json

def get_movie_detail(movie_url):
    """获取电影详细信息"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(movie_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取票房信息（如果有）
        box_office = "暂无数据"
        info_section = soup.find('div', id='info')
        if info_section:
            text = info_section.get_text()
            if '票房' in text:
                lines = text.split('\n')
                for line in lines:
                    if '票房' in line:
                        box_office = line.strip()
                        break

        # 获取重映年份（如果有）
        rerelease_years = []
        if info_section:
            release_dates = info_section.find_all('span', property='v:initialReleaseDate')
            for date in release_dates:
                year = date.text[:4]
                if year not in rerelease_years:
                    rerelease_years.append(year)

        # 获取前3条热评
        hot_comments = []
        comments_section = soup.find_all('div', class_='comment-item')
        for comment in comments_section[:3]:
            comment_text = comment.find('span', class_='short')
            if comment_text:
                hot_comments.append(comment_text.text.strip())

        # 获取海报
        poster = ""
        poster_tag = soup.find('div', id='mainpic')
        if poster_tag:
            img = poster_tag.find('img')
            if img and 'src' in img.attrs:
                poster = img['src']

        return {
            'box_office': box_office,
            'rerelease_years': ', '.join(rerelease_years) if len(rerelease_years) > 1 else '',
            'hot_comments': hot_comments,
            'poster': poster
        }
    except Exception as e:
        print(f"获取详细信息出错: {e}")
        return None

def scrape_douban_top250():
    """爬取豆瓣Top250电影"""
    base_url = "https://movie.douban.com/top250"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    movies = []

    # 豆瓣Top250共10页，每页25部电影
    for page in range(0, 250, 25):
        print(f"正在爬取第 {page//25 + 1} 页...")
        url = f"{base_url}?start={page}"

        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到所有电影条目
            movie_items = soup.find_all('div', class_='item')

            for item in movie_items:
                # 电影名称
                title = item.find('span', class_='title').text

                # 电影链接
                movie_url = item.find('a')['href']

                # 评分
                rating = item.find('span', class_='rating_num').text

                # 基本信息（年份、导演、主演等）
                info = item.find('div', class_='bd').find('p').text.strip()
                info_lines = [line.strip() for line in info.split('\n') if line.strip()]

                # 解析导演和主演
                director_actors = info_lines[0] if info_lines else ""
                director = ""
                actors = ""

                if '导演:' in director_actors:
                    parts = director_actors.split('主演:')
                    director = parts[0].replace('导演:', '').strip()
                    actors = parts[1].strip() if len(parts) > 1 else ""

                # 年份和地区
                year_info = info_lines[1] if len(info_lines) > 1 else ""
                year = year_info.split('/')[0].strip() if year_info else ""

                print(f"正在获取《{title}》的详细信息...")

                # 获取详细信息
                detail = get_movie_detail(movie_url)
                time.sleep(2)  # 礼貌性等待，避免请求过快

                movie_data = {
                    '排名': len(movies) + 1,
                    '电影名称': title,
                    '首次上映年份': year,
                    '重映年份': detail['rerelease_years'] if detail else '',
                    '评分': rating,
                    '导演': director,
                    '主演': actors,
                    '票房': detail['box_office'] if detail else '暂无数据',
                    '热评1': detail['hot_comments'][0] if detail and len(detail['hot_comments']) > 0 else '',
                    '热评2': detail['hot_comments'][1] if detail and len(detail['hot_comments']) > 1 else '',
                    '热评3': detail['hot_comments'][2] if detail and len(detail['hot_comments']) > 2 else '',
                    '海报链接': detail['poster'] if detail else '',
                    '豆瓣链接': movie_url
                }

                movies.append(movie_data)
                print(f"已完成: {len(movies)}/250")

        except Exception as e:
            print(f"爬取第 {page//25 + 1} 页出错: {e}")
            continue

    return movies

def save_to_csv(movies, filename='douban_top250.csv'):
    """保存为CSV文件"""
    if not movies:
        print("没有数据可保存")
        return

    keys = movies[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(movies)
    print(f"数据已保存到 {filename}")

def save_to_json(movies, filename='douban_top250.json'):
    """保存为JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {filename}")

if __name__ == "__main__":
    print("开始爬取豆瓣电影Top250...")
    print("预计需要10-15分钟，请耐心等待...")
    print("=" * 50)

    movies = scrape_douban_top250()

    print("=" * 50)
    print(f"爬取完成！共获取 {len(movies)} 部电影")

    # 保存数据
    save_to_csv(movies)
    save_to_json(movies)

    print("所有数据已保存！")