# DNS of dnschecker.org

- URL: <view-source:https://dnschecker.org/>
- Lines: 1039 - 1069
- Regex:
  - Match: `^<tr.+data-location="([^"]+)".+data-provider="([^"]+)".+(\n.+){2}data-clipboardtext="([^"]+)".+(\n.+){4}`
  - Replacement: `"$4":{"Location": "$1","Provider": "$2","DNS": "$4"},`
- Result:

```
Location: Mountain View CA, United States
Provider:  Google
DNS: 8.8.8.8

Location: Berkeley, US
Provider: Quad9
DNS: 9.9.9.9

Location: San Francisco CA, United States
Provider: OpenDNS
DNS: 208.67.222.220

Location: Miami, United States
Provider: AT&amp;T Services
DNS: 12.121.117.201

Location: Canoga Park, CA, United States
Provider:  Sprint
DNS: 204.117.214.10

Location: Dothan, United States
Provider: Comodo Secure DNS
DNS: 8.26.56.26

Location: San Francisco, US
Provider: Quad9
DNS: 149.112.112.112

Location: St. John's, Canada
Provider: Memorial University of Newfoundland
DNS: 134.153.233.140

Location: Yekaterinburg, Russian Federation
Provider:  Skydns
DNS: 195.46.39.39

Location: Cullinan, South Africa
Provider: Liquid Telecommunications Ltd
DNS: 5.11.11.5

Location: Roosendaal, Netherlands
Provider: NForce Entertainment B.V.
DNS: 185.107.80.84

Location: Paris, France
Provider: Online S.A.S.
DNS: 163.172.107.158

Location: Madrid, Spain
Provider: Prioritytelecom Spain S.A.
DNS: 212.230.255.1

Location: Zizers, Switzerland
Provider: Oskar Emmenegger
DNS: 194.209.157.109

Location: Innsbruck, Austria
Provider: nemox.net
DNS: 83.137.41.9

Location: Manchester, United Kingdom
Provider: Ancar B Technologies Ltd
DNS: 194.145.240.6

Location: Copenhagen, Denmark
Provider: Tele Danmark
DNS: 80.196.100.209

Location: Oberhausen, Germany
Provider: Verizon Deutschland GmbH
DNS: 194.172.160.4

Location: Tlalnepantla, Mexico
Provider: Uninet S.A. de C.V.
DNS: 148.235.82.66

Location: Santa Cruz do Sul, Brazil
Provider: Claro S.A
DNS: 200.248.178.54

Location: Kuala Lumpur, Malaysia
Provider: Ohana Communications Sdn Bhd
DNS: 103.26.250.4

Location: Research, Australia
Provider: Cloudflare Inc
DNS: 1.1.1.1

Location: Melbourne, Australia
Provider: Pacific Internet
DNS: 61.8.0.113

Location: Auckland, New Zealand
Provider: SiteHost
DNS: 223.165.64.97

Location: Singapore
Provider: T-systems Singapore Pte
DNS: 202.56.128.30

Location: Seoul, South Korea
Provider: LG Dacom Corporation
DNS: 164.124.101.2

Location: Hangzhou, China
Provider: Aliyun Computing Co. Ltd
DNS: 223.5.5.5

Location: Izmir, Turkey
Provider: Turk Telekom
DNS: 212.175.192.114

Location: Coimbatore, India
Provider: Skylink Fibernet Private Limited
DNS: 103.99.150.10

Location: Islamabad, Pakistan
Provider: CMPak Limited
DNS: 209.150.154.1

Location: Viana do Castelo, Portugal
Provider: CLOUDITY Network
DNS: 185.83.212.30

Location: Ireland
Provider: Daniel Cid
DNS: 185.228.168.9

Location: Kaharole, Bangladesh
Provider: Md Masud Rana Roni
DNS: 103.157.237.34
```