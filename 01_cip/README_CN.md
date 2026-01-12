# Akamai Tools: Check IP

使用 Python 库 `akadata` 调用 `Akamai Edgescape API` 进行 ip2location 查询

[English](./README.md)

## 0x00. 说明

- 通常情况下的文字是描述, 在方框中的文字是终端中运行的命令.

``` shell
# 框框里面的都是命令, 例如:
python3 --version

# 以 # 开头的都是注释, 可以不用复制
```

## 0x01. 环境

- Programing Language:
  - Python 3.8+
- Python Libs:
  - akadata
  - dnspython
  - requests

## 0x02. 安装步骤 How To Install

1. 安装 [Python 3.8+](https://www.python.org/downloads/).

   _**注意**_: Python3 在不同系统中的命令略有不同, Unix-like (Linux/MacOS, 本repo内简称 Unix, 下同) 为 `python3`, Windows 为 `python`, 因此Windows 环境下注意替换命令中的 `python3` 为 `python`.

   在终端中查看 Python 版本:

    ``` shell
    python3 --version
    ```

    输出:

    ``` Text
    Python 3.9.12
    ```

2. (内地) 配置 python 镜像源以加快 python 库安装.

    通过以下命令, 为 Python pypi 配置 南京大学 镜像源:

    ``` shell
    python3 -m pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple
    ```

3. 通过以下命令，为 Python 安装第三方库 akadata, dnspython, requests:

    ``` shell
    python3 -m pip install akadata dnspython requests
    ```

4. 修改配置文件:
   1. 复制 `01_cip/bin/config.example.ini` 为 `01_cip/bin/config.ini`.
   2. (可选) 设置解析文件的路径.
      - 针对安卓设备上运行的 Termux, 可以直接取消注释以下行:
      ``` ini
      ;resolv_path = /data/data/com.termux/files/usr/etc/resolv.conf
      ```
      - 如果你无法或者不想使用 /etc/resolv.conf 作为解析文件, 那么就将 resolv_path 设置为你希望使用的解析文件的路径.
   3. (可选) 修改 `[DEFAULT]` 中的 EdgeSacpe 服务器请求超时时间及字段显示信息.
   4. 修改 `[EDGESCAPE]` 中的 EdgeScape 服务器信息.
   5. 修改 `[UPDATE]` 中的 cip 更新服务器信息.
5. 以 cip.py 路径为 `/Users/user/git/akamai-tools/01_cip/bin/cip.py` 为例, 通过以下命令查看 cip 是否运行正常:

   ``` shell
   python3 /Users/user/git/akamai-tools/01_cip/bin/cip.py -i 1.1.1.1
   ```

   输出:

   ``` Text
   ===== SERVER: gcps-es.srip.net:21001
   ===== DNS: Local DNS
   1.1.1.1: [ region: Australia, region_code: NSW, city: SYDNEY, network: mil, company: APNIC_and_Cloudflare_DNS_Resolver_project, timezone: GMT+10, default_answer: N ]
   ```

6. 设置 alias
   - Unix
     以我的环境为例:
     - repo 对应 Shell 变量为 AK_TOOLS_HOME
     - 已经设置过该变量
     - cip文件的路径是 ${AK_TOOLS_HOME}/01_cip/bin/cip.py:
       1. 查看当前使用的终端:

          ``` shell
          echo ${SHELL}
          ```

          输出:

          ``` Text
          /bin/zsh
          ```

       2. 如果发现输出是 `/bin/bash`, 有两个选择:

          - (推荐) 更改默认终端为 `zsh`:
            - 运行命令:

              ``` shell
              chsh -s /bin/zsh
              ```

            - 重启电脑生效
          - 将 alias 配置在 ~/.bashrc 中 (有可能不生效)

       3. 我使用的是 zsh, 那么环境变量在 ~/.zshrc 中, 则在 ~/.zshrc 中添加如下行:

          ``` shell
          # 注意需要放在 export AK_TOOLS_HOME=.... 下面
          alias akcip="python3 ${AK_TOOLS_HOME}/01_cip/bin/cip.py"
          ```

       4. 重新打开 Terminal, 进行一次查询检查配置是否正常:

          ``` shell
          akcip -v
          ```

   - Windows
     1. 打开 PowerShell, 通过以下命令查看 PowerShell 配置文件路径:

        ``` PowerShell
        echo $PROFILE
        ```

        输出:

        ``` Text
        C:\Users\shengjyerao\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
        ```

        这是输出只是指明 PowerShell 通过读取这个文件的内容来加载自定义的内容，应该把自定义配置信息写在这个文件里面，但并不代表这个文件一定存在，没有这个文件时需要手动创建。

     2. 以文件路径 "C:\Users\shengjyerao\git\akamai-tools\01_cip\bin\cip.py" 为例。
       通过vscode打开上面获取到的 PowerShell 配置文件, 添加以下内容并保存:

        ``` PowerShell
        function akcip {
            python.exe "C:\Users\shengjyerao\git\akamai-tools\01_cip\bin\cip.py" $args
        }
        ```

     3. 重新打开 PowerShell, 检查 cip 命令是否正常

        ``` PowerShell
        akcip -v
        ```

## 0x03. 功能菜单

| 参数          | 说明                                                | 样例                                                 |
| :------------ | :-------------------------------------------------- | :--------------------------------------------------- |
| 无 / h / help | 显示帮助                                            |                                                      |
| i / input     | 对 -i 之后的内容作为输入进行查询.                   | -i 1.1.1.1                                           |
|               | 多个值之间以空格分隔.                               | -i 1.1.1.1 pstools.akamai.com                        |
| f / file      | 以文件作为输入进行查询, 并将查询结果追加到该文件内. | -f /Users/user/iptest-1.txt                          |
|               | 多个文件名之间以空格分隔.                           | -f /Users/user/iptest-1.txt /Users/user/iptest-2.txt |
| d / dns       | 使用指定的 DNS 解析域名, 未指定时使用 Local DNS.    | -d 8.8.8.8                                           |
|               | 多个 DNS 以空格分割.                                | -d 8.8.8.8 1.1.1.1                                   |
| l             | 查看当前版本更新日志.                               |                                                      |
| log           | 查看所有版本更新日志.                               |                                                      |
| u / update    | 更新 cip                                            |                                                      |
| v             | 查看 cip 版本信息                                   |                                                      |
| version       | 查看 cip 详细版本信息                               |                                                      |

## 0x04. 样例

- 查询 IP
  - 输入:

    ``` shell
    akcip -i 1.1.1.1 2.2.2.2
    ```

  - 输出:

    ``` shell
    ===== SERVER: es.server.com:2001
    ===== DNS: Local DNS
    1.1.1.1: [ country_code: AU, region_code: NSW, city: SYDNEY, network: mil, company: APNIC_and_Cloudflare_DNS_Resolver_project, timezone: GMT+10, default_answer: N ]
    2.2.2.2: [ country_code: TW, city: TAIPEI, network: francetelecom, company: Orange/France_Telecom, timezone: GMT+8, default_answer: N ]
    ```

- 查询域名 (Local DNS):
  - 输入:

    ``` shell
    akcip -i www.akamai.com pstools.akamai.com
    ```

  - 输出:

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

- 查询域名 (指定 DNS):
  - 输入:

    ``` shell
    akcip -i www.akamai.com pstools.akamai.com -d 8.8.8.8
    ```

  - 输出:

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

## 0x05. 其他

- 如果发现在查询过程中存在 "Request error of xxx: timed out", 那就是请求去 EdgeScape server 失败了, 重试即可
