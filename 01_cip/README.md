# Akamai Tools: Check IP

Check location info of IP with Python lib: `akadata` via `Akamai Edgescape API`

[中文](./README_CN.md)

## 0x00. Introduction

- Almost all the text are description but the text in square are commands need to run in terminal.

``` shell
# All the text in square are commands like:
python3 --version

# But the text start with # are note, which can be ignored when copy the commands
```

## 0x01. Program & Packges

- Programing Language:
  - Python 3.8+
- Python Libs:
  - akadata
  - dnspython
  - requests

## 0x02. How To Install

1. Install [Python 3.8+](https://www.python.org/downloads/).

   _**Note**_: The commands of python may different depends on the Systems, like the `python3` on Unix-like (Linux/MacOS, called Unix in this repo), and `python` on Windows, so remember to replace the `python3` with `python` on Windows.

   Check the version of Python in terminal:

    ``` shell
    python3 --version
    ```

    Output:

    ``` Text
    Python 3.9.12
    ```

2. (China Mainland) Set up the mirror lib of Python to speed up the lib install.

    Set up Nanjing University as mirror of Python pypi:

    ``` shell
    python3 -m pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple
    ```

3. Install Python libs: akadata, dnspython, requests:

    ``` shell
    python3 -m pip install akadata dnspython requests
    ```

4. Update the config file:
   1. Copy the `01_cip/bin/config.example.ini` to `01_cip/bin/config.ini`.
   2. (Optional) Edit the resolve config file path.
      - For Termux on Android, just uncomment the line: 
      ``` ini
      ;resolv_path = /data/data/com.termux/files/usr/etc/resolv.conf
      ```
      - If you can't or you don't want to use /etc/resolv.conf as the resolve file, set the values of resolv_path which the path of resolv file you want to use.
   3. (Optional) Edit the Timeout and Field limit in section: `[DEFAULT]`.
   4. Edit the server info of EdgeScape in the section: `[EDGESCAPE]`.
   5. Edit the server info of update in section: `[UPDATE]`
5. For e.g. the path `cip.py` is `/Users/user/git/akamai-tools/01_cip/bin/cip.py`, validate the cip works or not:

   ``` shell
   python3 /Users/user/git/akamai-tools/01_cip/bin/cip.py -i 1.1.1.1
   ```

   Output:

   ``` Text
   ===== SERVER: es.server.com:21001
   ===== DNS: Local DNS
   1.1.1.1: [ region: Australia, region_code: NSW, city: SYDNEY, network: mil, company: APNIC_and_Cloudflare_DNS_Resolver_project, timezone: GMT+10, default_answer: N ]
   ```

6. Set up alias
   - Unix
     For example:
     - The shell variable of this repo is `AK_TOOLS_HOME`
     - Already setup the variable
     - The path of `cip` is `${AK_TOOLS_HOME}/01_cip/bin/cip.py`:
       1. Check the shell which we are using:

          ``` shell
          echo ${SHELL}
          ```

          Output:

          ``` Text
          /bin/zsh
          ```

       2. We have 2 options if output is `/bin/bash`:

          - (Recommond) Change the default shell to `zsh`:
            - Run command:

              ``` shell
              chsh -s /bin/zsh
              ```

            - Restart the computer
          - Setup alias in ~/.bashrc (May not works!)

       3. The shell I using is `zsh`, so I need to update the `~/.zshrc` to add the following lines:

          ``` shell
          # Remeber add the lines below export AK_TOOLS_HOME=....
          alias akcip="python3 ${AK_TOOLS_HOME}/01_cip/bin/cip.py"
          ```

       4. Re-open the Terminal to check if the alias works:

          ``` shell
          akcip -v
          ```

   - Windows
     1. Start PowerShell and check the path of PowerShell config:

        ``` PowerShell
        echo $PROFILE
        ```

        Output:

        ``` Text
        C:\Users\shengjyerao\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
        ```

        Note: The output only shows the config path that PowerShell will load from but the file may not exist at yet. We need to create one if file not exist.

     2. For example, the path of `cip.py` is "C:\Users\shengjyerao\git\akamai-tools\01_cip\bin\cip.py":
        Create a PowerShell config with following lines:

        ``` PowerShell
        function akcip {
            python.exe "C:\Users\shengjyerao\git\akamai-tools\01_cip\bin\cip.py" $args
        }
        ```

     3. Re-open PowerShell and check `cip` works or not:

        ``` PowerShell
        akcip -v
        ```

## 0x03. Menu

| Args                | Note                                                 | Example                                              |
| :------------------ | :--------------------------------------------------- | :--------------------------------------------------- |
| No Args / h / help | Display help                                         |                                                      |
| i / input           | Lookup the arg(s) after -i                         | -i 1.1.1.1                                           |
|                     | Split with whitespace for multiple values.           | -i 1.1.1.1 pstools.akamai.com                        |
| f / file            | Lookup the content of file and add the result to it. | -f /Users/user/iptest-1.txt                          |
|                     | Split with whitespace for multiple files.            | -f /Users/user/iptest-1.txt /Users/user/iptest-2.txt |
| d / dns             | DNS server, use `Local DNS` if not used.             | -d 8.8.8.8                                           |
|                     | Split with whitespace for multiple servers.          | -d 8.8.8.8 1.1.1.1                                   |
| l                   | Check the log of current version.                    |                                                      |
| log                 | Check the log of all version.                        |                                                      |
| u / update          | Update cip                                           |                                                      |
| v                   | Check the version info (short) of cip                |                                                      |
| version             | Check the version info (detail) of cip               |                                                      |

## 0x04. Demo

- IP lookup
  - Input:

    ``` shell
    akcip -i 1.1.1.1 2.2.2.2
    ```

  - Output:

    ``` shell
    ===== SERVER: es.server.com:2001
    ===== DNS: Local DNS
    1.1.1.1: [ country_code: AU, region_code: NSW, city: SYDNEY, network: mil, company: APNIC_and_Cloudflare_DNS_Resolver_project, timezone: GMT+10, default_answer: N ]
    2.2.2.2: [ country_code: TW, city: TAIPEI, network: francetelecom, company: Orange/France_Telecom, timezone: GMT+8, default_answer: N ]
    ```

- Domain lookup (Local DNS):
  - Input:

    ``` shell
    akcip -i www.akamai.com pstools.akamai.com
    ```

  - Output:

    ``` Text
    ===== SERVER: es.server.com:2001
    ===== DNS: Local DNS
    =================== www.akamai.com ===================
    122.224.46.78: [ country_code: CN, region_code: ZJ, city: SHAOXING, network: chinanet, company: MoveInternet_Network_Technology_Co._Ltd., timezone: GMT+8, default_answer: N ]
    =================== www.akamai.com ===================
    ================= pstools.akamai.com =================
    115.152.253.89: [ country_code: CN, region_code: JX, city: JINGDEZHEN, network: chinanet, company: CHINANET_JIANGXI_PROVINCE_NETWORK, timezone: GMT+8, default_answer: N ]
    ================= pstools.akamai.com =================
    ```

- Domain lookup (specific DNS):
  - Input:

    ``` shell
    akcip -i www.akamai.com pstools.akamai.com -d 8.8.8.8
    ```

  - Output:

    ``` Text
    ===== SERVER: es.server.com:2001
    ===== DNS: ['8.8.8.8']
    =================== www.akamai.com ===================
    61.147.219.242: [ country_code: CN, region_code: JS, city: NANTONG, company: CHINANET_jiangsu_province_network, timezone: GMT+8, default_answer: N ]
    =================== www.akamai.com ===================
    ================= pstools.akamai.com =================
    218.91.224.43: [ country_code: CN, region_code: JS, city: NANTONG, company: CHINANET_jiangsu_province_network, timezone: GMT+8, default_answer: N ]
    ================= pstools.akamai.com =================
    ```

## 0x05. Others

- If the messages shows: "Request error of xxx: timed out" as result means request timeout of the EdgeScape server, just retry for more times.
