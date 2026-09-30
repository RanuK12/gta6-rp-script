import requests
import json
import sys
import time
from bs4 import BeautifulSoup

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
    # The snapshot returns JSON, we need to find the HTML content.
    # Let's first see what the snapshot contains by printing a sample? 
    # But we can't print in the middle of the loop for all. We'll assume it has a field 'html' or 'content'.
    # If not, we'll look for a string that looks like HTML.
    html = ''
    if isinstance(snapshot, dict):
        # Try common field names
        for key in ['html', 'content', 'body', 'source']:
            if key in snapshot and isinstance(snapshot[key], str):
                html = snapshot[key]
                break
        # If not found, maybe the entire snapshot is the HTML? Unlikely.
        if not html:
            # Convert the whole dict to string and see if it contains HTML
            snapshot_str = json.dumps(snapshot)
            if '<html' in snapshot_str or '<body' in snapshot_str:
                html = snapshot_str
    elif isinstance(snapshot, str):
        html = snapshot
    
    if not html:
        # If we still don't have HTML, we can't parse.
        print("Warning: Could not extract HTML from snapshot", file=sys.stderr)
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    threads = soup.select('.topic-list-item')
    results = []
    for t in threads[:5]:  # top 5
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
        snapshot = get_snapshot(tab_id)
        results = extract_topics(snapshot)
        return results
    finally:
        if tab_id:
            close_tab(tab_id)

if __name__ == '__main__':
    candidates = [
        ("NPC memory AI", "fivem npc memory script"),
        ("Housing 2.0 physics", "fivem housing script physics"),
        ("Cartel economy", "fivem drug cartel economy script"),
        ("Hitman contracts", "fivem hitman contract script"),
        ("Elite tuners", "fivem tuner script premium"),
        ("Gang territory", "fivem gang territory script"),
        ("Immersive hospital", "fivem hospital roleplay script"),
        ("Influencer system", "fivem influencer script"),
        ("Fishing & maritime", "fivem fishing script"),
        ("Prison break", "fivem prison break script")
    ]
    
    for cand_name, query in candidates:
        print(f"Processing: {cand_name} -> {query}")
        results = search_query(query)
        # Create a markdown file with the results
        # Convert candidate name to a safe filename
        safe_name = cand_name.lower().replace(' ', '_').replace('&', '').replace('.', '')
        out_file = f"docs/research/{safe_name}.md"
        with open(out_file, 'w') as f:
            f.write(f"# Search results for: {query}\n\n")
            f.write(f"## Candidate: {cand_name}\n\n")
            if not results:
                f.write("No results found.\n")
            else:
                f.write("| Title | URL | Replies | Views | Last Post Date |\n")
                f.write("|-------|-----|---------|-------|----------------|\n")
                for r in results:
                    f.write(f"| {r['title']} | {r['url']} | {r['replies']} | {r['views']} | {r['last_post_date']} |\n")
            f.write("\n")
        # Also save raw JSON for debugging
        json_file = f"docs/research/{safe_name}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        # Be respectful
        time.sleep(2)