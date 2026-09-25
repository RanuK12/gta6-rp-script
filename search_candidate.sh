#!/usr/bin/env bash
query="$1"
safe_query=$(echo "$query" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
url="https://forum.cfx.re/search?q=$(echo "$query" | sed 's/ /+/g')"

echo "=== $query ===" >> ~/.ranukita/projects/gta6-rp-script/docs/research/raw.txt
echo "$url" >> ~/.ranukita/projects/gta6-rp-script/docs/research/raw.txt

# Fetch the search results page
html=$(curl -sS -H "Accept: text/html" "$url" --max-time 15)
echo "$html" >> ~/.ranukita/projects/gta6-rp-script/docs/research/raw.txt
echo "" >> ~/.ranukita/projects/gta6-rp-script/docs/research/raw.txt

# Also save raw HTML for each candidate
echo "$html" > ~/.ranukita/projects/gta6-rp-script/docs/research/${safe_query}.html