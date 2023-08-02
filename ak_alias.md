# Alias

## VS codes

``` shell
alias ch="code /etc/hosts"
alias czp="code ${HOME}/.zprofile"
```

## Akamai Headers

``` shell
export AK_HEADER="Pragma: akamai-x-get-request-id, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-cache-tags, akamai-x-get-true-cache-key, akamai-x-serial-no"
export AK_HEADERE="Pragma: akamai-x-get-request-id, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-cache-tags, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-extracted-values"
```

## cURL alias

``` shell
# curl: HEAD
alias curli="curl -I"
# curl: HEAD with Akamai Pragma Headers
alias curlia="curl -I -H \"${AK_HEADER}\""
# curl: HEAD with Akamai Pragma Headers with akamai-x-get-extracted-values
alias curliae="curl -I -H \"${AK_HEADERE}\""
# curl: GET with response headers and response body
alias curls="curl -s -S -D -"
# curl: like curlia
alias curlsa="curl -s -S -D - -H \"${AK_HEADER}\""
# curl: like curliae
alias curlsae="curl -s -S -D - -H \"${AK_HEADERE}\""
# curl: GET with response headers but without response body
alias curln="curl -s -S -D - -o /dev/null"
# curl: like curlia
alias curlna="curl -s -S -D - -o /dev/null -H \"${AK_HEADER}\""
# curl: like curliae
alias curlnae="curl -s -S -D - -o /dev/null -H \"${AK_HEADERE}\""
```

## dig

```shell
alias ds="dig +short"
alias da="dig +noall +answer"
```

## Set / Unset proxy in terminal

``` shell
alias proxyset="export ALL_PROXY=\"http://proxy_server:port\""
alias proxyuns="unset ALL_PROXY"
```

## (MacOS) Flush DNS

``` shell
alias dnsflush="dscacheutil -flushcache"
```
