#!/bin/bash

CONCURRENT=2
TESTS=100
UAS=("examBot" )
PROTO=http
DOMAIN=-exam.yourstore.com
PATHS="/"
EDGE_HOST=a1.g.akamai-staging.net
EDGE_PORT=80

for ua in "${UAS[@]}"; do
  /usr/bin/ab -v 0 -q -S -d -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS  -H "cookie:partNumber=yZCV7Zvty4dW"  -H "User-Agent: $ua" "$PROTO://$USER$DOMAIN$PATHS"
done


#transparent
ua=""
/usr/bin/ab -v 0 -q -S -d -i -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS -H "User-Agent: $ua"  "$PROTO://$USER$DOMAIN$PATHS"
#active
ua="evilBot"
/usr/bin/ab -v 0 -q -S -d -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS  -H "cookie:ak_bmsc=123" -H "User-Agent: $ua" "$PROTO://$USER$DOMAIN$PATHS"

echo "Generating traffic (please be patient)"

for i in {1..100}; do
/usr/bin/curl -s -S --connect-to "$USER$DOMAIN":"$EDGE_PORT":"$EDGE_HOST":"$EDGE_PORT" \
"http://$USER$DOMAIN/index.php?route=account/login" \
-H "authority: $USER$DOMAIN" \
-H 'pragma: no-cache'   -H 'cache-control: no-cache' \
-H 'accept: application/json, text/plain, */*' \
-H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36' \
-H 'content-type: application/json' \
-H "origin: http://$USER$DOMAIN" \
-H 'sec-fetch-site: same-origin' \
-H 'sec-fetch-mode: cors' \
-H 'sec-fetch-dest: empty' \
-H "referer: http://$USER$DOMAIN/" \
-H 'accept-language: en-US,en;q=0.9,es;q=0.8' \
-H 'cookie: language=en; welcomebanner_status=dismiss;  io=H1-9Vtxayp4pdpaQAABZ' \
--data-binary '{"email":"a","password":"a"}' \
--compressed \
-o /dev/null;

done

echo "Finished"
