#!/usr/bin/env bash
QUERY="$1"
URL="https://forum.cfx.re/search?q=${QUERY// /%20}"
curl -s "$URL" | grep -E 'data-topic-id' | head -5 > /tmp/ids.txt
# Para cada id obtener métricas (simplificado: usar API de Discourse)
while read -r id; do
    API="https://forum.cfx.re/t/${id}.json"
    data=$(curl -s "$API")
    replies=$(echo "$data" | jq '.reply_count')
    views=$(echo "$data" | jq '.views')
    date=$(echo "$data" | jq '.posts[0].created_at' | cut -dT -f1)
    price=$(echo "$data" | jq '.description | match("\\$[0-9]+") | .string' | tr -d '"')
    echo "| $QUERY | $id | $replies | $views | $date | $price |" >> /tmp/results.md
done < /tmp/ids.txt