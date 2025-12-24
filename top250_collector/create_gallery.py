"""
项目名称：豆瓣光影画廊 (Douban Movie Gallery) - 全平台完美适配版
更新内容：
    1. 电脑端：恢复大卡片布局 (最小宽度 220px)，拒绝拥挤。
    2. 手机端：保持双列布局 (最小宽度 140px)，精致紧凑。
    3. 交互优化：电脑有悬停特效，手机点击直接跳转。
"""

import json
import os

def create_html():
    # 获取当前脚本路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'douban_top250.json')
    html_path = os.path.join(current_dir, 'movie_gallery.html')
    posters_dir = os.path.join(current_dir, 'posters')

    # 1. 读取数据
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            movies = json.load(f)
    except FileNotFoundError:
        print(f"❌ 错误：找不到 {json_path}")
        return

    # 2. HTML 头部样式
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>豆瓣电影 Top 250 收藏夹</title>
        <style>
            * { box-sizing: border-box; }
            
            body { 
                background-color: #121212; 
                color: #e0e0e0; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
            }
            
            h1 { 
                text-align: center; 
                color: #ffc107; 
                margin: 30px 0 40px 0; 
                font-size: 28px;
                letter-spacing: 2px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }
            
            /* --- 搜索框样式 --- */
            .search-box { 
                text-align: center; 
                margin-bottom: 40px; 
                position: sticky; 
                top: 20px; 
                z-index: 100; 
            }
            
            input { 
                padding: 15px 25px; 
                width: 100%; 
                max-width: 600px; 
                border-radius: 30px; 
                border: 1px solid #444; 
                background: rgba(40, 40, 40, 0.9); 
                color: #fff;
                outline: none; 
                font-size: 16px; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                transition: all 0.3s;
            }
            
            input:focus { 
                border-color: #ffc107; 
                box-shadow: 0 8px 20px rgba(255, 193, 7, 0.2);
                transform: scale(1.02);
            }

            /* --- 核心布局逻辑 (PC优先) --- */
            .grid { 
                display: grid; 
                /* 电脑端默认：每张卡片至少 220px 宽，这样看起来很大气，不拥挤 */
                grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); 
                gap: 30px; 
                padding-bottom: 60px;
                max-width: 1400px; /* 限制最大宽度，防止在大宽屏上太散 */
                margin: 0 auto;
            }
            
            /* --- 卡片样式 --- */
            .card { 
                background: #1e1e1e; 
                border-radius: 12px; 
                overflow: hidden; 
                position: relative; 
                display: block; 
                text-decoration: none; 
                color: #fff; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .poster-box { width: 100%; aspect-ratio: 2/3; overflow: hidden; }
            .poster-box img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }

            .info { padding: 18px; }
            
            .rank-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
            .rank { background: #ffc107; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 12px; }
            .rating { color: #ff9800; font-weight: bold; font-size: 15px; }
            
            h3 { margin: 8px 0; font-size: 17px; line-height: 1.4; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .year { font-size: 13px; color: #888; }
            
            /* --- 电脑端悬停遮罩层 --- */
            .overlay {
                position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.9); 
                padding: 25px;
                opacity: 0; 
                transition: opacity 0.3s;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .overlay p { font-size: 14px; margin: 6px 0; color: #ccc; line-height: 1.6; }
            .overlay .comment { margin-top: 15px; font-style: italic; color: #fff; border-left: 3px solid #ffc107; padding-left: 10px; }

            /* 电脑端鼠标交互 */
            @media (hover: hover) {
                .card:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.5); z-index: 10; }
                .card:hover .overlay { opacity: 1; }
                .card:hover img { transform: scale(1.1); }
            }

            /* --- 📱 移动端专属规则 (屏幕小于 768px 时生效) --- */
            @media (max-width: 768px) {
                body { padding: 10px; }
                h1 { font-size: 22px; margin: 20px 0; }
                
                .search-box { top: 10px; margin-bottom: 20px; }
                input { padding: 10px 20px; font-size: 14px; }

                .grid { 
                    /* 手机端强制调整：卡片变小到 140px，间距变小，确保一行能放两个 */
                    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); 
                    gap: 12px; 
                }
                
                .card { border-radius: 8px; }
                .info { padding: 10px; }
                h3 { font-size: 14px; }
                .rating { font-size: 12px; }
                .year { font-size: 11px; }

                /* 手机上去掉遮罩层，点击直接跳转 */
                .overlay { display: none !important; }
            }
        </style>
    </head>
    <body>
        <h1>🎬 豆瓣 Top 250 光影画廊</h1>
        
        <div class="search-box">
            <input type="text" id="searchInput" onkeyup="filterMovies()" placeholder="🔍 搜索电影名 / 导演...">
        </div>

        <div class="grid" id="movieGrid">
    """

    # 3. 循环生成
    for movie in movies:
        clean_name = movie['电影名称'].replace('/', '_').replace(':', '_').replace(' ', '_')
        image_relative_path = f"posters/{clean_name}.jpg"
        image_abs_path = os.path.join(posters_dir, f"{clean_name}.jpg")
        
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
                    <div class="rank-row">
                        <span class="rank">No.{movie['排名']}</span>
                        <span class="rating">★ {movie['评分']}</span>
                    </div>
                    <h3>{movie['电影名称']}</h3>
                    <div class="year">{movie['首次上映年份']}</div>
                </div>
                
                <div class="overlay">
                    <h3 style="color:#ffc107; margin-bottom:15px">{movie['电影名称']}</h3>
                    <p>导演: {movie['导演'].split(' ')[0]}</p>
                    <p>主演: {movie['主演'][:12]}...</p>
                    <p class="comment">“{movie['热评1'][:50]}...”</p>
                    <div style="margin-top:auto; text-align:center; background:#333; padding:8px; border-radius:20px; font-size:12px; color:#ffc107">
                        点击查看豆瓣详情 ↗
                    </div>
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
                var cards = document.getElementsByClassName('card');

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

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ 完美适配版网页已生成！")
    print("现在无论在 27寸大屏 还是 iPhone 上查看，效果都是最佳的。")

if __name__ == "__main__":
    create_html()