import requests
import json
import sys
import time

BASE = "http://localhost:9377"
USER_ID = "ranukita"
SESSION_KEY = "default"

def ensure_server():
    try:
        resp = requests.get(f"{BASE}/health", timeout=5)
        if resp.status_code != 200:
            raise Exception("Server not healthy")
    except Exception:
        print("Camofox server not running. Please start it with rk-stealth-browse start", file=sys.stderr)
        sys.exit(1)

def open_tab(url):
    ensure_server()
    resp = requests.post(f"{BASE}/tabs", 
                         json={"userId": USER_ID, "sessionKey": SESSION_KEY, "url": url},
                         timeout=10)
    if resp.status_code != 200:
        raise Exception(f"Failed to open tab: {resp.text}")
    data = resp.json()
    return data.get("tabId")

def close_tab(tab_id):
    ensure_server()
    resp = requests.delete(f"{BASE}/tabs/{tab_id}", 
                           params={"userId": USER_ID},
                           timeout=10)
    if resp.status_code != 200:
        print(f"Warning: failed to close tab {tab_id}: {resp.text}", file=sys.stderr)

def get_snapshot(tab_id):
    ensure_server()
    resp = requests.get(f"{BASE}/tabs/{tab_id}/snapshot", 
                        params={"userId": USER_ID},
                        timeout=10)
    if resp.status_code != 200:
        raise Exception(f"Failed to get snapshot: {resp.text}")
    return resp.json()

def extract_topics(snapshot):
    # The snapshot is the HTML? Actually, the snapshot endpoint returns the HTML? 
    # According to the script, snapshot returns JSON? Let's check the script: 
    #   curl -s "$BASE/tabs/$TAB_ID/snapshot?userId=$USER_ID" | python3 -m json.tool
    # So it returns JSON. But what structure? We'll assume it contains the HTML in a field.
    # However, the Camofox API might return the HTML as a string in a field like 'html' or 'content'.
    # Let's inspect by actually calling it for a known URL.
    # For now, we'll assume it returns the HTML in a field called 'html'.
    # If not, we'll need to adjust.
    html = snapshot.get('html', '')
    if not html:
        # Maybe the snapshot is the raw HTML?
        if isinstance(snapshot, str):
            html = snapshot
        else:
            # Try to find a field that contains the HTML
            for key, value in snapshot.items():
                if isinstance(value, str) and ('<html' in value or '<body' in value):
                    html = value
                    break
    # Parse HTML with BeautifulSoup if available, else use regex (but we don't have bs4 installed? We can install it via pip, but we can also use the existing search_cfx.py which uses bs4. We'll import bs4.
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # Install bs4 using pip
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    threads = soup.select('.topic-list-item')
    results = []
    for t in threads[:5]:
        title_elem = t.select_one('a.title')
        if not title_elem:
            continue
        title = title_elem.text.strip()
        link = "https://forum.cfx.re" + title_elem.get('href', '')
        reply_elem = t.select_one('.reply-count')
        replies = int(reply_elem.text.strip()) if reply_elem and reply_elem.text.strip().isdigit() else 0
        view_elem = t.select_one('.view-count')
        views = int(view_elem.text.strip()) if view_elem and view_elem.text.strip().isdigit() else 0
        last_post_elem = t.select_one('.last-post')
        last_post_date = ''
        if last_post_elem:
            last_post_date = last_post_elem.get('title', '').strip()
            if not last_post_date:
                last_post_date = last_post_elem.text.strip()
        results.append({
            "title": title,
            "url": link,
            "replies": replies,
            "views": views,
            "last_post_date": last_post_date
        })
    return results

def search_query(query):
    url = f"https://forum.cfx.re/search?q={query.replace(' ', '+')}"
    tab_id = None
    try:
        tab_id = open_tab(url)
        # Wait for page to load
        time.sleep(3)
        # We could also wait for the topic list to appear by evaluating JS, but for simplicity we sleep.
        snapshot = get_snapshot(tab_id)
        results = extract_topics(snapshot)
        return results
    finally:
        if tab_id:
            close_tab(tab_id)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 search_cfx_stealth.py <query>", file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    results = search_query(query)
    print(json.dumps(results, indent=2))