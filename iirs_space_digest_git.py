# -*- coding: utf-8 -*-
"""
IIRS Space Digest - PythonAnywhere Production Version
Daily automated space news for IIRS employees
"""

import feedparser
import re
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

print("🚀 Starting IIRS Daily Space Digest...")

# Verified working space agency RSS feeds
feeds = [
    'https://www.esa.int/rss/rss-topnews.xml',  # ESA space missions
    'https://www.esa.int/rss/programmes.xml',        # Ariane/vegla
    'https://www.esa.int/rss/space_science.xml',     # JUICE/PLATO missions
    'https://www.esa.int/rss/earth_observation.xml', # Sentinel satellites
    'https://www.nasa.gov/rss/dyn/breaking_news.rss', # NASA updates
    'https://www.nasa.gov/rss/dyn/images_of_the_day.rss', # Satellite images
    'https://www.space.com/feeds/all',            # Space.com main
    'https://spaceflightnow.com/feed/',           # Launch updates
    'https://phys.org/rss-feed/space-news/',      # Physics.org space
    'https://www.thespacereview.com/rss.xml',     # Weekly analysis
    'https://interestingengineering.com/feed',    # Tech breakthroughs
]



def extract_first_image_url(html_content):
    """✅ Extract first clean image URL from RSS HTML"""
    if not html_content:
        return None
    img_patterns = [
        r'<img[^>]+src=["\']([^"\']+\.(jpg|jpeg|png|gif|webp))["\'][^>]*>',
        r'<media:content[^>]+url=["\']([^"\']+)["\'][^>]*>',
        r'<enclosure[^>]+url=["\']([^"\']+)["\'][^>]*>'
    ]
    for pattern in img_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            img_url = match.group(1)
            if img_url.startswith('http') and len(img_url) > 20:
                return img_url
    return None

def sanitize_html_content(text):
    """✅ Strip HTML but preserve line breaks"""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text[:380] + '...' if len(text) > 380 else text.strip()

# ✅ Generate news digest (ERROR HANDLING ADDED)
news_digest = []
print("📡 Fetching space news from 11 sources...")
for url in feeds:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
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
    except Exception as e:
        print(f"⚠️ Skip {url}: {e}")

print(f"✅ Fetched {len(news_digest)} news items")

# Generate beautiful HTML newsletter
timestamp = date.today().strftime("%d-%m-%Y")
html_body = f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ box-sizing: border-box !important; }}
html, body {{
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}}
body {{
    font-family: Arial, sans-serif !important;
    max-width: 900px !important;
    margin: 20px auto !important;
    background: #f8fafc !important;
    padding: 25px !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
}}
.content-wrapper {{
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 0 !important;
}}
.scroll-container {{
    flex: 1 !important;
    max-height: 85vh !important;
    height: calc(100vh - 220px) !important;
    width: 100% !important;
    max-width: 880px !important;
    margin: 0 auto !important;
    overflow-y: auto !important;
    overflow-x: auto !important;
    scrollbar-width: thin !important;
    scrollbar-color: #3b82f6 #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 20px !important;
    background: #fafbfc !important;
}}
.news-card {{
    display: block !important;
    width: 100% !important;
    margin-bottom: 35px !important;
    padding: 0 !important;
}}
.card-content {{
    background: white !important;
    border-left: 4px solid #3b82f6 !important;
    border-radius: 12px !important;
    padding: 25px !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
    margin: 0 !important;
    min-height: 180px !important;
}}
.card-image {{
    width: 100% !important;
    height: 140px !important;
    object-fit: cover !important;
    border-radius: 8px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    display: block !important;
}}
.card-title {{
    margin: 0 0 12px 0 !important;
    font-size: 18px !important;
    line-height: 1.4 !important;
}}
.card-source {{
    color: #555 !important;
    margin: 0 0 16px 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}}
.card-summary {{
    color: #333 !important;
    line-height: 1.7 !important;
    margin: 0 0 20px 0 !important;
    font-size: 15px !important;
    border-left: 2px solid #e5e7eb !important;
    padding: 15px !important;
    background: #f8fafc !important;
    border-radius: 6px !important;
}}
.read-more {{
    display: inline-block !important;
    color: #3b82f6 !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    padding: 8px 16px !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 6px !important;
}}
.scroll-spacer {{ height: 60px !important; display: block !important; }}
.footer {{ margin-top: auto !important; }}
.scroll-container::-webkit-scrollbar {{ width: 8px !important; height: 12px !important; }}
.scroll-container::-webkit-scrollbar-track {{ background: #f1f5f9 !important; border-radius: 4px !important; }}
.scroll-container::-webkit-scrollbar-thumb {{ background: #3b82f6 !important; border-radius: 4px !important; }}
.scroll-container::-webkit-scrollbar-corner {{ background: #f1f5f9 !important; height: 12px !important; }}
</style>
</head>
<body>
<h2 style='color:#1e3a8a;border-bottom:3px solid #3b82f6;padding-bottom:10px;margin-bottom:25px'>🚀 IIRS - Daily Space News Digest</h2>
<p style='color:#666;margin-bottom:20px'><i>{timestamp} | {len(news_digest)} Space Tech Updates</i></p>

<div class="content-wrapper">
    <div class="scroll-container">
""" + "".join([f"""
        <div class="news-card">
            <div class="card-content">
                (f'<img src="{item.get("image", "")}" alt="Space news image" class="card-image" loading="lazy">' if item.get("image") else '')
                <div class="card-title">
                    <a href="{item['link']}" target="_blank" style="color:#1e40af;text-decoration:none;font-weight:600">{i}. {item['title']}</a>
                </div>
                <div class="card-source">{item['source']}</div>
                <div class="card-summary">{item['summary']}</div>
                <a href="{item['link']}" target="_blank" class="read-more">Read Full Article →</a>
            </div>
        </div>
""" for i, item in enumerate(news_digest, 1)]) + """
        <div class="scroll-spacer"></div>
    </div>
</div>

<div class="footer">
    <p style='text-align:center;color:#888;border-top:1px solid #eee;padding-top:25px'>
        <small>IIRS Library | Indian Institute of Remote Sensing | Dehradun</small>
    </p>
</div>
</body>
</html>
"""

# ✅ Save timestamped HTML file (PythonAnywhere compatible)
filename = f'iirs_news_{date.today().strftime("%Y%m%d")}.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html_body)

print(f"✅ SAVED: {filename} with {len(news_digest)} items")
print(f"📁 View at: https://ashshbsht.pythonanywhere.com/files/home/ashshbsht/{filename}")
print("🎉 Ready for GitHub Actions email!")
