import requests, bs4, json, sys, time, re
from urllib.parse import quote_plus

def search_forum(query):
    url = f"https://forum.cfx.re/search?q={quote_plus(query)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Search error for {query}: {e}")
        return []
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    threads = soup.select('.topic-list-item')
    results = []
    for t in threads[:5]:  # top 5
        link_el = t.select_one('a.title')
        if not link_el:
            continue
        link = "https://forum.cfx.re" + link_el.get('href')
        title = link_el.text.strip()
        replies_el = t.select_one('.reply-count')
        views_el = t.select_one('.view-count')
        replies = int(replies_el.text.strip()) if replies_el and replies_el.text.strip().isdigit() else 0
        views = int(views_el.text.strip()) if views_el and views_el.text.strip().isdigit() else 0
        # fetch thread page for price and last post date
        price = None
        last_post = None
        try:
            rt = requests.get(link, headers=headers, timeout=10)
            rt.raise_for_status()
            soup_t = bs4.BeautifulSoup(rt.text, 'html.parser')
            # look for price patterns
            text = soup_t.get_text()
            # price like $25, $15.00, etc.
            price_match = re.search(r'\\$\\s*(\\d+(?:\\.\\d+)?)', text)
            if price_match:
                price = float(price_match.group(1))
            # also look for tebex.io or creator.tebex.io
            if not price:
                tebex_link = soup_t.find('a', href=re.compile(r'tebex\\.io|creator\\.tebex\\.io'))
                if tebex_link:
                    price = "Tebex link present"
            # last post date: look for relative time or date
            # simplest: find timestamp
            time_el = soup_t.select_one('time[datetime]')
            if time_el and time_el.has_attr('datetime'):
                last_post = time_el['datetime']
            else:
                # look for class containing 'ago'
                ago_el = soup_t.select_one('.relative-date, .timestamp-ago')
                if ago_el:
                    last_post = ago_el.text.strip()
        except Exception as e:
            # if cannot fetch, leave price/last_post as None
            pass
        results.append({
            "title": title,
            "url": link,
            "replies": replies,
            "views": views,
            "price": price,
            "last_post": last_post
        })
        time.sleep(1)  # be polite
    return results

def main():
    candidates = [
        "fivem npc memory script",
        "fivem housing script physics",
        "fivem drug cartel economy script",
        "fivem hitman contract script",
        "fivem tuner script premium",
        "fivem gang territory script",
        "fivem hospital roleplay script",
        "fivem influencer script",
        "fivem fishing script",
        "fivem prison break script"
    ]
    all_data = {}
    for q in candidates:
        print(f"Processing: {q}")
        results = search_forum(q)
        # derive candidate name from second word
        name = q.split()[1] if len(q.split()) > 1 else q.replace(' ', '_')
        all_data[name] = results
        # save individual file
        import os
        os.makedirs('docs/research', exist_ok=True)
        with open(f'docs/research/{name}.json', 'w') as f:
            json.dump(results, f, indent=2)
        # also create a markdown summary
        with open(f'docs/research/{name}.md', 'w') as f:
            f.write(f'# Research for {q}\\n\\n')
            if not results:
                f.write('No results found.\\n')
            else:
                f.write(f'Found {len(results)} threads.\\n\\n')
                for i, r in enumerate(results, 1):
                    f.write(f'## {i}. {r["title"]}\\n')
                    f.write(f'- URL: {r["url"]}\\n')
                    f.write(f'- Replies: {r["replies"]}\\n')
                    f.write(f'- Views: {r["views"]}\\n')
                    f.write(f'- Price: {r["price"] if r["price"] is not None else "Not found"}\\n')
                    f.write(f'- Last post: {r["last_post"] if r["last_post"] is not None else "Not found"}\\n\\n')
        time.sleep(2)
    # save combined
    with open('docs/research/all.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    print("Research complete.")

if __name__ == '__main__':
    main()