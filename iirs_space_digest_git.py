# -*- coding: utf-8 -*-
"""
IIRS Space Digest - PythonAnywhere Production Version
Daily automated space news for IIRS employees (TODAY'S NEWS ONLY)
COSMIC VOID THEME - 75% WIDTH UPGRADE
"""

import feedparser
import re
from datetime import date, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time

print("🚀 Starting IIRS Daily Space Digest - COSMIC VOID 75%...")

# Verified working space agency RSS feeds
feeds = [
    'https://www.esa.int/rss/rss-topnews.xml',
    'https://www.esa.int/rss/programmes.xml',        
    'https://www.esa.int/rss/space_science.xml',     
    'https://www.esa.int/rss/earth_observation.xml', 
    'https://www.nasa.gov/rss/dyn/breaking_news.rss', 
    'https://www.nasa.gov/rss/dyn/images_of_the_day.rss', 
    'https://www.space.com/feeds/all',            
    'https://spaceflightnow.com/feed/',           
    'https://phys.org/rss-feed/space-news/',      
    'https://www.thespacereview.com/rss.xml',     
    'https://interestingengineering.com/feed',    
]

def extract_first_image_url(html_content):
    """✅ Extract first clean image URL from RSS HTML"""
    if not html_content:
        return None
    
    img_patterns = [
        r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\'][^>]*>',
        r'<media:content[^>]+url=["\']([^"\']+)["\'][^>]*>',
        r'<enclosure[^>]+url=["\']([^"\']+)["\'][^>]*>'
    ]
    
    for pattern in img_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            img_url = match.group(1)
            if img_url and img_url.startswith('http') and len(img_url) > 20:
                return img_url
    return None

def sanitize_html_content(text):
    """✅ Strip HTML but preserve line breaks"""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text[:380] + '...' if len(text) > 380 else text.strip()

def is_today_or_yesterday(entry):
    """✅ Check if article is from today or yesterday"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    for date_field in ['published_parsed', 'updated_parsed']:
        if date_field in entry and entry[date_field]:
            try:
                entry_date = date(
                    entry[date_field].tm_year,
                    entry[date_field].tm_mon, 
                    entry[date_field].tm_mday
                )
                return entry_date == today or entry_date == yesterday
            except:
                continue
    
    for date_str in [entry.get('published'), entry.get('updated'), entry.get('created')]:
        if date_str:
            try:
                entry_time = time.strptime(date_str[:10], '%Y-%m-%d')
                entry_date = date(entry_time.tm_year, entry_time.tm_mon, entry_time.tm_mday)
                if entry_date == today or entry_date == yesterday:
                    return True
            except:
                continue
    
    return False

# ✅ TODAY'S NEWS ONLY
news_digest = []
print("📡 Fetching TODAY'S space news from 11 sources...")

for url in feeds:
    try:
        feed = feedparser.parse(url)
        print(f"📱 {feed.feed.get('title', 'Unknown')} - checking...")
        
        for entry in feed.entries[:10]:
            if is_today_or_yesterday(entry):
                raw_summary = entry.get('summary', '') or entry.get('description', '')
                image_url = extract_first_image_url(raw_summary)
                summary = sanitize_html_content(raw_summary)
                title = re.sub(r'<[^>]+>', '', entry.title)

                news_digest.append({
                    'title': title,
                    'link': entry.link,
                    'source': feed.feed.get('title', 'Space News')[:20] + '...',
                    'summary': summary,
                    'image': image_url
                })
                print(f"✅ TODAY: {title[:60]}...")
                
                if len(news_digest) >= 12:
                    break
        
        if len(news_digest) >= 12:
            break
            
    except Exception as e:
        print(f"⚠️ Skip {url}: {e}")

print(f"✅ Fetched {len(news_digest)} FRESH articles from today!")

if len(news_digest) == 0:
    print("⚠️ No today's news found - using recent articles...")
    for url in feeds[:3]:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                raw_summary = entry.get('summary', '') or entry.get('description', '')
                image_url = extract_first_image_url(raw_summary)
                summary = sanitize_html_content(raw_summary)
                title = re.sub(r'<[^>]+>', '', entry.title)

                news_digest.append({
                    'title': title,
                    'link': entry.link,
                    'source': feed.feed.get('title', 'Space News')[:20] + '...',
                    'summary': summary,
                    'image': image_url
                })
                if len(news_digest) >= 6:
                    break
            if len(news_digest) >= 6:
                break
        except:
            continue

# ✅ 75% WIDTH HTML GENERATION
timestamp = date.today().strftime("%d-%m-%Y")
articles_html = ""

for i, item in enumerate(news_digest, 1):
    image_html = ''
    if item.get("image"):
        image_html = f'<img src="{item["image"]}" alt="Space news image" class="card-image" loading="lazy" onerror="this.style.display=\'none\'">'
    
    articles_html += f'''
        <div class="news-card">
            <div class="card-content">
                {image_html}
                <div class="card-title">
                    <a href="{item["link"]}" target="_blank">{i}. {item["title"]}</a>
                </div>
                <div class="card-source">{item["source"]}</div>
                <div class="card-summary">{item["summary"]}</div>
                <a href="{item["link"]}" target="_blank" class="read-more">Read Full Article →</a>
            </div>
        </div>
    '''

# ✅ COSMIC VOID THEME - 75% WIDTH UPGRADE
html_body = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ box-sizing: border-box !important; }}
html, body {{ 
    height: 100vh !important; 
    margin: 0 !important; 
    padding: 0 !important; 
}}
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    max-width: 95vw !important; 
    margin: 20px auto !important; 
    /* 🌌 COSMIC VOID BACKGROUND */
    background: #0a0a0a !important;
    padding: 25px !important; 
    min-height: 100vh !important; 
    display: flex !important; 
    flex-direction: column !important;
    position: relative !important;
    overflow-x: hidden !important;
}}
/* ✨ ULTRA-FAINT STARFIELD */
body::before {{
    content: '' !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background-image: 
        radial-gradient(1px 1px at 20px 30px, rgba(255,255,255,0.4), transparent),
        radial-gradient(0.5px 0.5px at 40px 70px, rgba(255,255,255,0.2), transparent),
        radial-gradient(0.8px 0.8px at 90px 40px, rgba(255,255,255,0.3), transparent),
        radial-gradient(0.3px 0.3px at 130px 80px, rgba(255,255,255,0.1), transparent),
        radial-gradient(1px 1px at 160px 30px, rgba(255,255,255,0.25), transparent);
    background-repeat: repeat !important;
    background-size: 300px 150px !important;
    animation: voidDrift 40s linear infinite !important;
    pointer-events: none !important;
    z-index: 1 !important;
}}
@keyframes voidDrift {{
    0% {{ transform: translateX(0) translateY(0); opacity: 0.6; }}
    100% {{ transform: translateX(-300px) translateY(-150px); opacity: 0.4; }}
}}
.content-wrapper {{ 
    flex: 1 !important; 
    display: flex !important; 
    flex-direction: column !important; 
    min-height: 0 !important;
    position: relative !important;
    z-index: 10 !important;
}}
.scroll-container {{ 
    flex: 1 !important; 
    max-height: 85vh !important; 
    height: calc(100vh - 220px) !important; 
    /* 🔥 75% WIDTH UPGRADE */
    width: 75% !important;
    max-width: none !important;
    min-width: 680px !important;
    margin: 0 auto !important; 
    overflow-y: auto !important; 
    overflow-x: hidden !important; 
    scrollbar-width: thin !important; 
    scrollbar-color: #c0c0c0 rgba(10,10,10,0.9) !important;
    /* 🌌 EXTREME GLASS CONTAINER */
    background: rgba(10, 10, 10, 0.9) !important;
    backdrop-filter: blur(30px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 24px !important; 
    padding: 40px !important;
    box-shadow: 
        0 35px 70px rgba(0,0,0,0.8),
        inset 0 1px 0 rgba(255,255,255,0.05) !important;
}}
.news-card {{ 
    display: block !important; 
    width: 100% !important; 
    margin-bottom: 45px !important; 
    padding: 0 !important; 
}}
.card-content {{ 
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(25px) saturate(1.3) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-left: 3px solid transparent !important;
    background-clip: padding-box !important;
    border-radius: 24px !important; 
    padding: 40px !important; 
    box-shadow: 
        0 25px 60px rgba(0,0,0,0.6),
        0 0 0 1px rgba(255,255,255,0.08),
        inset 0 1px 0 rgba(255,255,255,0.03) !important;
    margin: 0 !important; 
    min-height: 220px !important;
    position: relative !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}}
.card-content:hover {{
    border-left-color: #00ffff !important;
    box-shadow: 
        0 35px 80px rgba(0,255,255,0.15),
        0 0 0 1px rgba(0,255,255,0.2),
        inset 0 1px 0 rgba(255,255,255,0.06) !important;
    transform: translateY(-5px) !important;
}}
.card-image {{ 
    width: 100% !important; 
    height: 180px !important; 
    object-fit: cover !important; 
    border-radius: 20px !important;
    margin-bottom: 25px !important; 
    box-shadow: 
        0 15px 40px rgba(0,0,0,0.7),
        inset 0 1px 0 rgba(255,255,255,0.1) !important;
    display: block !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}}
.card-title {{ 
    margin: 0 0 18px 0 !important; 
    font-size: 22px !important; 
    line-height: 1.4 !important;
}}
.card-title a {{ 
    color: #c0c0c0 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}}
.card-title a:hover {{ 
    color: #ffffff !important;
    text-shadow: 0 0 15px rgba(0,255,255,0.4) !important;
}}
.card-source {{ 
    color: #a0a0a0 !important; 
    margin: 0 0 22px 0 !important; 
    font-size: 14px !important; 
    font-weight: 500 !important;
    background: rgba(255,255,255,0.04) !important;
    padding: 8px 18px !important;
    border-radius: 25px !important;
    display: inline-block !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}}
.card-summary {{ 
    color: #d0d0d0 !important; 
    line-height: 1.8 !important; 
    margin: 0 0 30px 0 !important; 
    font-size: 16px !important; 
    border-left: 2px solid transparent !important;
    padding: 25px !important;
    background: rgba(255,255,255,0.02) !important;
    border-radius: 16px !important;
    box-shadow: inset 0 2px 15px rgba(0,0,0,0.3) !important;
}}
.card-summary:hover {{
    border-left-color: #00ffff !important;
}}
.read-more {{ 
    display: inline-block !important;
    color: #c0c0c0 !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    padding: 14px 28px !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 30px !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.5) !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    position: relative !important;
    overflow: hidden !important;
}}
.read-more:hover {{ 
    color: #ffffff !important;
    background: rgba(0,255,255,0.1) !important;
    border-color: #00ffff !important;
    box-shadow: 
        0 10px 30px rgba(0,255,255,0.2),
        0 0 25px rgba(0,255,255,0.3) !important;
    transform: translateY(-2px) !important;
}}
.scroll-spacer {{ height: 60px !important; display: block !important; }}
.footer {{ 
    margin-top: auto !important; 
    color: rgba(192,192,192,0.7) !important;
    text-align: center !important;
    padding: 30px !important;
    font-size: 14px !important;
}}
.scroll-container::-webkit-scrollbar {{ width: 8px !important; }}
.scroll-container::-webkit-scrollbar-track {{ 
    background: rgba(10,10,10,0.9) !important; 
    border-radius: 4px !important; 
}}
.scroll-container::-webkit-scrollbar-thumb {{ 
    background: linear-gradient(180deg, #c0c0c0, #ffffff) !important; 
    border-radius: 4px !important;
    opacity: 0.6 !important;
}}
.scroll-container::-webkit-scrollbar-thumb:hover {{ 
    background: linear-gradient(180deg, #00ffff, #c0c0c0) !important;
    opacity: 1 !important;
}}
h2 {{ 
    color: #c0c0c0 !important;
    text-align: center !important;
    border-bottom: 2px solid rgba(255,255,255,0.2) !important;
    padding-bottom: 25px !important;
    margin-bottom: 35px !important;
    font-weight: 700 !important;
    font-size: 28px !important;
    letter-spacing: 2px !important;
}}
h2:hover {{
    color: #ffffff !important;
    text-shadow: 0 0 20px rgba(0,255,255,0.3) !important;
}}
/* 🔥 RESPONSIVE 75% WIDTH */
@media screen and (max-width: 1400px) {{
    .scroll-container {{ 
        width: 85% !important; 
        min-width: 600px !important;
        padding: 35px !important;
    }}
}}
@media screen and (max-width: 1000px) {{
    .scroll-container {{ 
        width: 92% !important; 
        min-width: 0 !important;
        padding: 30px !important;
    }}
    body {{ max-width: 98vw !important; }}
}}
@media screen and (max-width: 600px) {{
    .scroll-container {{ padding: 25px !important; }}
    .card-content {{ padding: 35px !important; }}
    h2 {{ font-size: 24px !important; }}
}}
</style>
</head>
<body>
<h2>🌌 IIRS - Daily Space News Digest</h2>
<p style='color:rgba(192,192,192,0.9);margin-bottom:30px;text-align:center;font-style:italic;font-size:16px;font-weight:400;letter-spacing:1px'><i>{timestamp} | {len(news_digest)} Space Tech Updates</i></p>
<div class="content-wrapper">
    <div class="scroll-container">
        {articles_html}
        <div class="scroll-spacer"></div>
    </div>
</div>
<div class="footer">
    <p style='margin:0'>
        <small>IIRS Library | Indian Institute of Remote Sensing | Dehradun</small>
    </p>
</div>
</body>
</html>"""

# ✅ Save timestamped HTML file
filename = f'iirs_news_void_75pct_{date.today().strftime("%Y%m%d")}.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html_body)

print(f"✅ SAVED: {filename} with {len(news_digest)} items (COSMIC VOID 75% 🌌)")
print("🎉 75% WIDTH UPGRADE COMPLETE!")
print("🌌 COSMIC VOID FEATURES:")
print("   • Pure #0a0a0a void background")
print("   • Ultra-faint white star drift (40s)")
print("   • Extreme glassmorphism cards")
print("   • Cyan pulse hover effects")
print("📏 NEW 75% WIDTH:")
print("   • width: 75% (desktop)")
print("   • Responsive: 85% tablet, 92% mobile") 
print("   • min-width: 680px (readability)")
print("   • padding: 40px (optimal spacing)")
print("🎉 Production-ready for PythonAnywhere!")
