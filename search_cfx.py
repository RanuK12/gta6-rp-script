import requests
import json
import sys
import time

def search_cfx(query):
    url = f"https://forum.cfx.re/search.json?q={query.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        results = []
        posts = data.get('posts', [])
        
        for post in posts[:5]:  # top 5
            topic_id = post.get('topic_id')
            if topic_id:
                link = f"https://forum.cfx.re/t/{topic_id}"
                title = post.get('blurb', '').split('\n')[0][:100]  # First line, truncated
                reply_count = post.get('reply_count', 0)
                views = post.get('views', 0)
                created_at = post.get('created_at', '')
                
                results.append({
                    "title": title,
                    "url": link,
                    "replies": reply_count,
                    "views": views,
                    "created_at": created_at
                })
        
        return results
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_cfx.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    results = search_cfx(query)
    print(json.dumps(results, indent=2))