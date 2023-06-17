#!/bin/bash

CONCURRENT=2
TESTS=100
PROTO=https
DOMAIN=my-proshop.com
PATH="/"
EDGE_HOST=my-proshop.edgekey-staging.net
EDGE_PORT=443

echo "Generating Bot traffic (please be patient)"
for i in {1..100}; do
/usr/bin/curl -s -S --connect-to "$USER.$DOMAIN":"$EDGE_PORT":"$EDGE_HOST":"$EDGE_PORT" \
"https://$USER.$DOMAIN/rest/user/login" \
-H "authority: $USER.$DOMAIN" \
-H 'pragma: no-cache'   -H 'cache-control: no-cache' \
-H 'accept: application/json, text/plain, */*' \
-H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36' \
-H 'content-type: application/json' \
-H "origin: https://$USER.$DOMAIN" \
-H 'sec-fetch-site: same-origin' \
-H 'sec-fetch-mode: cors' \
-H 'sec-fetch-dest: empty' \
-H "referer: https://$USER.$DOMAIN/" \
-H 'accept-language: en-US,en;q=0.9,es;q=0.8' \
-H 'cookie: language=en; welcomebanner_status=dismiss;  io=H1-9Vtxayp4pdpaQAABZ' \
--data-binary '{"email":"a","password":"a"}' \
--compressed \
-o /dev/null;

done

echo "Finished"
