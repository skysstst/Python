"""
项目名称：豆瓣光影画廊 (Douban Movie Gallery)
功能描述：
    读取 douban_top250.json 数据
    配合 posters 文件夹里的图片
    自动生成一个可视化的 HTML 网页海报墙
    
作者：Gemini User
日期：2025-12
"""

import json
import os

def create_html():
    # --- 核心修改：获取当前脚本所在的绝对路径 ---
    # 这样无论你在哪里运行命令，文件都会生成在脚本旁边的文件夹里
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建 json 文件的完整路径
    json_path = os.path.join(current_dir, 'douban_top250.json')
    # 构建 html 文件的完整路径
    html_path = os.path.join(current_dir, 'movie_gallery.html')
    # posters 文件夹的路径
    posters_dir = os.path.join(current_dir, 'posters')

    # 1. 读取数据
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            movies = json.load(f)
    except FileNotFoundError:
        print(f"❌ 错误：在 {current_dir} 目录下找不到 douban_top250.json")
        print("请确保 json 文件和这个脚本在同一个文件夹内！")
        return

    # 2. HTML 头部样式
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>豆瓣电影 Top 250 收藏夹</title>
        <style>
            body { background-color: #1a1a1a; color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            h1 { text-align: center; color: #ffc107; margin-bottom: 30px; }
            .search-box { text-align: center; margin-bottom: 40px; }
            input { padding: 10px 20px; width: 300px; border-radius: 20px; border: none; outline: none; font-size: 16px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 25px; padding: 0 40px; }
            .card { 
                background: #2d2d2d; border-radius: 10px; overflow: hidden; transition: transform 0.3s; position: relative; 
                display: block; text-decoration: none; color: #fff; 
            }
            .card:hover { transform: translateY(-10px); box-shadow: 0 10px 20px rgba(0,0,0,0.5); z-index: 10; }
            .poster-box { width: 100%; height: 300px; overflow: hidden; }
            .poster-box img { width: 100%; height: 100%; object-fit: cover; }
            .info { padding: 15px; }
            .rank { background: #ffc107; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
            .rating { float: right; color: #ffc107; font-weight: bold; }
            h3 { margin: 10px 0 5px 0; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            p { font-size: 12px; color: #aaa; margin: 5px 0; }
            .overlay {
                position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.9); padding: 20px;
                opacity: 0; transition: 0.3s;
                overflow-y: auto;
            }
            .card:hover .overlay { opacity: 1; }
            .comment { font-style: italic; color: #ddd; font-size: 13px; line-height: 1.5; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>🎬 豆瓣电影 Top 250 个人数据库</h1>
        <div class="search-box">
            <input type="text" id="searchInput" onkeyup="filterMovies()" placeholder="🔍 搜索电影名称、导演...">
        </div>
        <div class="grid" id="movieGrid">
    """

    # 3. 循环生成
    for movie in movies:
        clean_name = movie['电影名称'].replace('/', '_').replace(':', '_').replace(' ', '_')
        # 这是写在 HTML 里的相对路径，只要 HTML 和 posters 文件夹在一起就能显示
        image_relative_path = f"posters/{clean_name}.jpg"
        
        # 检查本地图片是否存在的绝对路径
        image_abs_path = os.path.join(posters_dir, f"{clean_name}.jpg")
        
        # 如果本地没有这张图，就用网络链接
        final_src = image_relative_path
        if not os.path.exists(image_abs_path):
            final_src = movie['海报链接'] 

        douban_link = movie.get('豆瓣链接', '#')

        card_html = f"""
            <a href="{douban_link}" target="_blank" class="card" data-title="{movie['电影名称']}" data-director="{movie['导演']}">
                <div class="poster-box">
                    <img src="{final_src}" loading="lazy" alt="{movie['电影名称']}">
                </div>
                <div class="info">
                    <span class="rank">No.{movie['排名']}</span>
                    <span class="rating">★ {movie['评分']}</span>
                    <h3>{movie['电影名称']}</h3>
                    <p>{movie['首次上映年份']}</p>
                </div>
                <div class="overlay">
                    <h3>{movie['电影名称']} 🔗</h3> 
                    <p>👉 点击跳转豆瓣详情</p>
                    <hr style="border-color:#444">
                    <p>导演: {movie['导演'].split(' ')[0]}</p>
                    <p>主演: {movie['主演'][:15]}...</p>
                    <p class="comment">“{movie['热评1']}”</p>
                </div>
            </a>
        """
        html_content += card_html

    # 4. 结尾 JS
    html_content += """
        </div>
        <script>
            function filterMovies() {
                var input = document.getElementById('searchInput');
                var filter = input.value.toUpperCase();
                var grid = document.getElementById("movieGrid");
                var cards = grid.getElementsByClassName('card');
                for (var i = 0; i < cards.length; i++) {
                    var title = cards[i].getAttribute('data-title');
                    var director = cards[i].getAttribute('data-director');
                    if (title.toUpperCase().indexOf(filter) > -1 || director.toUpperCase().indexOf(filter) > -1) {
                        cards[i].style.display = "";
                    } else {
                        cards[i].style.display = "none";
                    }
                }
            }
        </script>
    </body>
    </html>
    """

    # 5. 写入文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ 成功！")
    print(f"网页已生成在: {html_path}")

if __name__ == "__main__":
    create_html()