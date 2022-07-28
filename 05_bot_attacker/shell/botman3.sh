#!/bin/bash

CONCURRENT=2
TESTS=100
UAS=("PartnerJailBot" )
PROTO=https
DOMAIN=my-proshop.com
PATHS="/"
EDGE_HOST=my-proshop.edgekey-staging.net
EDGE_PORT=443

for ua in "${UAS[@]}"; do
  /usr/bin/ab -v 0 -q -S -d -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS  -H "cookie:partNumber=DWJhAXa22XkL"  -H "User-Agent: $ua" "$PROTO://$USER.$DOMAIN$PATHS"
  /usr/bin/ab -v 0 -q -S -d -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS  -H "cookie:partNumber=wrongValue"  -H "User-Agent: $ua" "$PROTO://$USER.$DOMAIN$PATHS"
done
