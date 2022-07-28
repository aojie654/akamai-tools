#!/bin/bash

CONCURRENT=2
TESTS=100
PROTO=https
DOMAIN=my-proshop.com
PATH="/"
EDGE_HOST=my-proshop.edgekey-staging.net
EDGE_PORT=443

#transparent
ua="BaiduSpider"
/usr/bin/ab -v 0 -q -S -d -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS -H "User-Agent: $ua" "$PROTO://$USER.$DOMAIN$PATH"
#active
ua="evilBot"
/usr/bin/ab -v 0 -q -S -d -X "$EDGE_HOST:$EDGE_PORT" -c$CONCURRENT -n$TESTS  -H "cookie:ak_bmsc=123" -H "User-Agent: $ua" "$PROTO://$USER.$DOMAIN$PATH"
