import feedparser
import json
import re
from datetime import datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader

MAX_ARTICLES = 25
SYDNEY_OFFSET = timedelta(hours=10)  # AEST (UTC+10); AEDT is +11


def clean_html(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_entry_date(entry):
    for attr in ('published_parsed', 'updated_parsed'):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.fromtimestamp(0, tz=timezone.utc)


def fetch_feed(feed_info):
    articles = []
    try:
        feed = feedparser.parse(
            feed_info['url'],
            request_headers={'User-Agent': 'Mozilla/5.0 cybersec-feed/1.0'}
        )
        for entry in feed.entries[:20]:
            url = entry.get('link', '').strip()
            if not url:
                continue
            title = clean_html(entry.get('title', '')).strip() or 'Untitled'
            raw = entry.get('summary', entry.get('description', ''))
            summary = clean_html(raw)
            if len(summary) > 320:
                summary = summary[:317].rsplit(' ', 1)[0] + '...'
            articles.append({
                'title': title,
                'url': url,
                'source': feed_info['name'],
                'date': parse_entry_date(entry),
                'summary': summary,
            })
    except Exception as exc:
        print(f"  [WARN] Failed to fetch {feed_info['name']}: {exc}")
    return articles


def build():
    with open('feeds.json', encoding='utf-8') as f:
        feeds = json.load(f)

    print(f"[*] Fetching {len(feeds)} feeds...")
    all_articles = []
    seen_urls = set()

    for feed_info in feeds:
        items = fetch_feed(feed_info)
        added = 0
        for item in items:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                all_articles.append(item)
                added += 1
        print(f"  [+] {feed_info['name']}: {added} new items")

    all_articles.sort(key=lambda a: a['date'], reverse=True)
    articles = all_articles[:MAX_ARTICLES]

    for a in articles:
        a['date_str'] = (
            a['date'].strftime('%Y-%m-%d %H:%M UTC')
            if a['date'].timestamp() > 0
            else 'Unknown date'
        )

    now_utc = datetime.now(timezone.utc)
    sydney_now = now_utc + SYDNEY_OFFSET
    generated_at = sydney_now.strftime('%Y-%m-%d %H:%M AEST')

    env = Environment(loader=FileSystemLoader('templates'), autoescape=True)
    template = env.get_template('index.html.jinja')
    html = template.render(
        articles=articles,
        generated_at=generated_at,
        article_count=len(articles),
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[+] Built index.html — {len(articles)} articles — updated {generated_at}")


if __name__ == '__main__':
    build()
