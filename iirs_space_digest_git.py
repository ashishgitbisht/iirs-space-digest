# -*- coding: utf-8 -*-
"""
IIRS Space Digest - PythonAnywhere Production Version
Daily automated space news for IIRS employees (TODAY'S NEWS ONLY)
COSMIC VOID THEME - 75% WIDTH + NIGHT MODE DEFAULT + FIXED LIGHT MODE ☀️🌙
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

print("🚀 Starting IIRS Daily Space Digest - COSMIC VOID 75% + FIXED LIGHT MODE...")

# [ALL FUNCTIONS AND RSS LOGIC IDENTICAL - NO CHANGES]
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
    if not html_content: return None
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
    if not text: return ''
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
                entry_date = date(entry[date_field].tm_year, entry[date_field].tm_mon, entry[date_field].tm_mday)
                return entry_date == today or entry_date == yesterday
            except: continue
    for date_str in [entry.get('published'), entry.get('updated'), entry.get('created')]:
        if date_str:
            try:
                entry_time = time.strptime(date_str[:10], '%Y-%m-%d')
                entry_date = date(entry_time.tm_year, entry_time.tm_mon, entry_time.tm_mday)
                if entry_date == today or entry_date == yesterday: return True
            except: continue
    return False

# [NEWS COLLECTION LOGIC - UNCHANGED]
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
                    'title': title, 'link': entry.link,
                    'source': feed.feed.get('title', 'Space News')[:20] + '...',
                    'summary': summary, 'image': image_url
                })
                print(f"✅ TODAY: {title[:60]}...")
                if len(news_digest) >= 12: break
        if len(news_digest) >= 12: break
    except Exception as e:
        print(f"⚠️ Skip {url}: {e}")

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
                    'title': title, 'link': entry.link,
                    'source': feed.feed.get('title', 'Space News')[:20] + '...',
                    'summary': summary, 'image': image_url
                })
                if len(news_digest) >= 6: break
            if len(news_digest) >= 6: break
        except: continue

# HTML GENERATION
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

# ✅ FIXED LIGHT MODE - NO DARK OUTER BACKGROUND
html_body = f"""<!DOCTYPE html>
<html data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
/* 🌌 NIGHT MODE CSS VARIABLES (ACTIVE BY DEFAULT) */
:root {{
    --bg-primary: #0a0a0a;
    --bg-secondary: rgba(10, 10, 10, 0.9);
    --card-bg: rgba(255,255,255,0.05);
    --card-summary: rgba(255,255,255,0.02);
    --text-primary: #c0c0c0;
    --text-secondary: #a0a0a0;
    --text-light: #d0d0d0;
    --text-white: #ffffff;
    --border-light: rgba(255,255,255,0.08);
    --border-card: rgba(255,255,255,0.1);
    --shadow-dark: rgba(0,0,0,0.8);
    --cyan-accent: #00ffff;
}}
[data-theme="light"] {{
    /* ✅ FIXED: FULL LIGHT BACKGROUND - NO DARK OUTER */
    --bg-primary: #f8fafc !important;
    --bg-secondary: rgba(255, 255, 255, 0.98) !important;
    --card-bg: rgba(255,255,255,0.95) !important;
    --card-summary: rgba(248, 250, 252, 0.8) !important;
    --text-primary: #1e293b !important;
    --text-secondary: #475569 !important;
    --text-light: #334155 !important;
    --text-white: #0f172a !important;
    --border-light: rgba(0,0,0,0.06) !important;
    --border-card: rgba(0,0,0,0.08) !important;
    --shadow-dark: rgba(0,0,0,0.1) !important;
    --cyan-accent: #00b8d4 !important;
}}

/* ✅ FIXED: NO DARK FLASH IN EITHER MODE */
* {{ box-sizing: border-box !important; }}
html {{ 
    background: var(--bg-primary) !important;
    min-height: 100vh !important;
}}
html, body {{ 
    height: 100vh !important; 
    margin: 0 !important; 
    padding: 0 !important; 
    transition: all 0.3s ease !important;
}}
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    max-width: 95vw !important; 
    margin: 20px auto !important; 
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    padding: 25px !important; 
    min-height: 100vh !important; 
    display: flex !important; 
    flex-direction: column !important;
    position: relative !important;
    overflow-x: hidden !important;
}}

/* ✨ STARFIELD - NIGHT MODE ONLY */
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
    opacity: 1 !important;
    transition: opacity 0.3s ease !important;
}}
[data-theme="light"] body::before {{ opacity: 0 !important; }}
@keyframes voidDrift {{
    0% {{ transform: translateX(0) translateY(0); opacity: 0.6; }}
    100% {{ transform: translateX(-300px) translateY(-150px); opacity: 0.4; }}
}}

/* ☀️🌙 THEME TOGGLE BUTTON */
.theme-toggle {{
    position: fixed !important;
    top: 25px !important;
    right: 25px !important;
    z-index: 1000 !important;
    width: 55px !important;
    height: 55px !important;
    border: none !important;
    border-radius: 50% !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 24px !important;
    color: #ffffff !important;
    box-shadow: 0 8px 25px var(--shadow-dark), 0 0 0 1px var(--border-light) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    backdrop-filter: blur(20px) !important;
    background: rgba(255,255,255,0.15) !important;
}}
.theme-toggle:hover {{
    transform: scale(1.1) rotate(180deg) !important;
    box-shadow: 0 15px 35px rgba(0,255,255,0.4), 0 0 0 1px var(--cyan-accent) !important;
}}
[data-theme="light"] .theme-toggle {{
    background: rgba(30,41,59,0.9) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
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
    width: 75% !important;
    max-width: none !important;
    min-width: 680px !important;
    margin: 0 auto !important; 
    overflow-y: auto !important; 
    overflow-x: hidden !important; 
    scrollbar-width: thin !important; 
    scrollbar-color: var(--text-primary) var(--bg-secondary) !important;
    background: var(--bg-secondary) !important;
    backdrop-filter: blur(30px) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 24px !important; 
    padding: 40px !important;
    box-shadow: 
        0 35px 70px var(--shadow-dark),
        inset 0 1px 0 var(--border-light) !important;
    transition: all 0.3s ease !important;
}}
.news-card {{ display: block !important; width: 100% !important; margin-bottom: 45px !important; padding: 0 !important; }}
.card-content {{ 
    background: var(--card-bg) !important;
    backdrop-filter: blur(25px) saturate(1.3) !important;
    border: 1px solid var(--border-card) !important;
    border-left: 3px solid transparent !important;
    background-clip: padding-box !important;
    border-radius: 24px !important; 
    padding: 40px !important; 
    box-shadow: 
        0 25px 60px var(--shadow-dark),
        0 0 0 1px var(--border-light),
        inset 0 1px 0 var(--border-card) !important;
    margin: 0 !important; 
    min-height: 220px !important;
    position: relative !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    color: var(--text-primary) !important;
}}
.card-content:hover {{
    border-left-color: var(--cyan-accent) !important;
    box-shadow: 
        0 35px 80px rgba(0,255,255,0.15),
        0 0 0 1px var(--cyan-accent),
        inset 0 1px 0 var(--border-card) !important;
    transform: translateY(-5px) !important;
}}
.card-image {{ 
    width: 100% !important; height: 180px !important; object-fit: cover !important; 
    border-radius: 20px !important; margin-bottom: 25px !important; 
    box-shadow: 0 15px 40px var(--shadow-dark), inset 0 1px 0 var(--border-light) !important;
    display: block !important; border: 1px solid var(--border-card) !important;
}}
.card-title {{ margin: 0 0 18px 0 !important; font-size: 22px !important; line-height: 1.4 !important; color: var(--text-primary) !important; }}
.card-title a {{ color: var(--text-primary) !important; text-decoration: none !important; font-weight: 600 !important; transition: all 0.3s ease !important; }}
.card-title a:hover {{ color: var(--text-white) !important; text-shadow: 0 0 15px rgba(0,255,255,0.4) !important; }}
.card-source {{ 
    color: var(--text-secondary) !important; margin: 0 0 22px 0 !important; font-size: 14px !important; font-weight: 500 !important;
    background: rgba(255,255,255,0.04) !important; padding: 8px 18px !important; border-radius: 25px !important; 
    display: inline-block !important; border: 1px solid var(--border-light) !important;
}}
.card-summary {{ 
    color: var(--text-light) !important; line-height: 1.8 !important; margin: 0 0 30px 0 !important; font-size: 16px !important; 
    border-left: 2px solid transparent !important; padding: 25px !important; background: var(--card-summary) !important;
    border-radius: 16px !important; box-shadow: inset 0 2px 15px var(--shadow-dark) !important;
}}
.card-summary:hover {{ border-left-color: var(--cyan-accent) !important; }}
.read-more {{ 
    display: inline-block !important; color: var(--text-primary) !important; font-weight: 600 !important; text-decoration: none !important;
    padding: 14px 28px !important; background: rgba(255,255,255,0.05) !important; border: 1px solid var(--border-card) !important;
    border-radius: 30px !important; box-shadow: 0 5px 20px var(--shadow-dark) !important; 
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important; position: relative !important; overflow: hidden !important;
}}
.read-more:hover {{ 
    color: var(--text-white) !important; background: rgba(0,255,255,0.1) !important; border-color: var(--cyan-accent) !important;
    box-shadow: 0 10px 30px rgba(0,255,255,0.2), 0 0 25px rgba(0,255,255,0.3) !important; transform: translateY(-2px) !important;
}}
.scroll-spacer {{ height: 60px !important; display: block !important; }}
.footer {{ margin-top: auto !important; color: var(--text-secondary) !important; text-align: center !important; padding: 30px !important; font-size: 14px !important; }}
.scroll-container::-webkit-scrollbar {{ width: 8px !important; }}
.scroll-container::-webkit-scrollbar-track {{ background: var(--bg-secondary) !important; border-radius: 4px !important; }}
.scroll-container::-webkit-scrollbar-thumb {{ background: linear-gradient(180deg, var(--text-primary), var(--text-white)) !important; border-radius: 4px !important; opacity: 0.6 !important; }}
.scroll-container::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(180deg, var(--cyan-accent), var(--text-primary)) !important; opacity: 1 !important; }}
h2 {{ color: var(--text-primary) !important; text-align: center !important; border-bottom: 2px solid var(--border-light) !important; padding-bottom: 25px !important; margin-bottom: 35px !important; font-weight: 700 !important; font-size: 28px !important; letter-spacing: 2px !important; }}
h2:hover {{ color: var(--text-white) !important; text-shadow: 0 0 20px rgba(0,255,255,0.3) !important; }}
@media screen and (max-width: 1400px) {{ .scroll-container {{ width: 85% !important; min-width: 600px !important; padding: 35px !important; }} }}
@media screen and (max-width: 1000px) {{ .scroll-container {{ width: 92% !important; min-width: 0 !important; padding: 30px !important; }} body {{ max-width: 98vw !important; }} }}
@media screen and (max-width: 600px) {{ .scroll-container {{ padding: 25px !important; }} .card-content {{ padding: 35px !important; }} h2 {{ font-size: 24px !important; }} .theme-toggle {{ width: 50px !important; height: 50px !important; font-size: 20px !important; }} }}
</style>
</head>
<body>
<!-- ☀️🌙 THEME TOGGLE BUTTON -->
<button class="theme-toggle" id="themeToggle" title="Switch to Light Mode">☀️</button>

<h2>🌌 IIRS - Daily Space News Digest</h2>
<p style='color:var(--text-secondary);margin-bottom:30px;text-align:center;font-style:italic;font-size:16px;font-weight:400;letter-spacing:1px'><i>{timestamp} | {len(news_digest)} Space Tech Updates</i></p>
<div class="content-wrapper">
    <div class="scroll-container">
        {articles_html}
        <div class="scroll-spacer"></div>
    </div>
</div>
<div class="footer">
    <p style='margin:0'><small>IIRS Library | Indian Institute of Remote Sensing | Dehradun</small></p>
</div>

<script>
/* ✅ NIGHT MODE BY DEFAULT + FIXED LIGHT MODE */
document.addEventListener('DOMContentLoaded', function() {{
    const html = document.documentElement;
    const toggleBtn = document.getElementById('themeToggle');
    
    function setNightMode() {{
        html.setAttribute('data-theme', 'dark');
        toggleBtn.textContent = '☀️';
        toggleBtn.title = 'Switch to Light Mode';
        localStorage.setItem('theme', 'dark');
    }}
    
    function setDayMode() {{
        html.setAttribute('data-theme', 'light');
        toggleBtn.textContent = '🌙';
        toggleBtn.title = 'Switch to Dark Mode';
        localStorage.setItem('theme', 'light');
    }}
    
    // Load saved theme or default to NIGHT MODE
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {{
        setDayMode();
    }} else {{
        setNightMode();  // ✅ DEFAULT: NIGHT MODE
    }}
    
    toggleBtn.addEventListener('click', function() {{
        if (html.getAttribute('data-theme') === 'dark') {{
            setDayMode();
        }} else {{
            setNightMode();
        }}
    }});
}});
</script>
</body>
</html>"""

filename = f'iirs_news_void_75pct_fixed_light_{date.today().strftime("%Y%m%d")}.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html_body)

print(f"✅ SAVED: {filename} with {len(news_digest)} items (LIGHT MODE FIXED ☀️🌙)")
print("🎉 LIGHT MODE DARK BACKGROUND ISSUE FIXED!")
print("🔧 KEY FIXES:")
print("   • html { background: var(--bg-primary) !important; }")
print("   • Light mode: #f8fafc solid white (NO gradient)")
print("   • !important on ALL light mode variables")
print("   • Full coverage: html + body backgrounds")
print("🌌 Night mode: Pure cosmic void #0a0a0a")
print("☀️ Light mode: Clean #f8fafc white")
print("📱 75% responsive width preserved")
