# Akamai Tools: dig

使用 Python 库 `dnspython` 进行多 DNS 解析

[English Doc](./README.md)

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
  - dnspython

## 0x02. 安装步骤

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
    通过以下命令, 为 Python pypi 配置 清华大学 镜像源:

    ``` shell
    python3 -m pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple
    ```

3. 通过以下命令，为 Python 安装第三方库 dnspython:

    ``` shell
    python3 -m pip install dnspython
    ```

4. 修改配置文件:
   1. 复制 `06_dig/conf/dns.example.json` 为 `06_dig/conf/dns.json`
   2. (可选) 根据个人喜好, 按照格式修改 DNS 服务器列表
   3. (可选) 如果你无法或者不想使用默认的解析文件 `/etc/resolv.conf`, 可以在配置文件中设置 resolv_path 变量的值:
      - 对于 Termux on Android
        ``` json
        {
            "resolv_path": "/data/data/com.termux/files/usr/etc/resolv.conf",
            "208.67.222.220": {
                "DNS": "208.67.222.220",
                "Location": "San Francisco CA, United States",
                "Provider": "OpenDNS"
            }
        }
        ```
      - 对于其他配置文件路径, 假设为 `/path/to/your/resolv/config`:
        ``` json
        {
            "resolv_path": "/path/to/your/resolv/config",
            "208.67.222.220": {
                "DNS": "208.67.222.220",
                "Location": "San Francisco CA, United States",
                "Provider": "OpenDNS"
            }
        }
        ```
5. 以 dig.py 路径为 `/Users/user/git/akamai-tools/06_dig/bin/dig.py` 为例, 通过以下命令查看 dig 是否运行正常:

   ``` shell
   python3 /Users/user/git/akamai-tools/06_dig/bin/dig.py -i www.example.com
   ```

   输出:

   ``` shell
    Working on hostname: www.example.com of DNS: 127.0.0.1, result: 93.184.216.34
    Working on hostname: www.example.com of DNS: 8.8.8.8, result: 93.184.216.34

        ====> Result:
        {
        "json": {
            "www.example.com": {
                "127.0.0.1": {
                    "DNS": "127.0.0.1",
                    "Location": "Local",
                    "Provider": "Local ISP",
                    "Result": "93.184.216.34"
                },
                "8.8.8.8": {
                    "DNS": "8.8.8.8",
                    "Location": "Mountain View CA, United States",
                    "Provider": "Google",
                    "Result": "93.184.216.34"
                }
            }
        }
    }
   ```

6. 设置 alias
   - Unix
     以我的环境为例:
     - repo 对应 Shell 变量为 AK_TOOLS_HOME
     - 已经设置过该变量
     - dig 文件的路径是 ${AK_TOOLS_HOME}/06_dig/bin/dig.py:
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
          alias akdig="python3 ${AK_TOOLS_HOME}/06_dig/bin/dig.py"
          ```

       4. 重新打开 Terminal, 进行一次查询检查配置是否正常:

          ``` shell
          akdig -v
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

     2. 以文件路径 "C:\Users\shengjyerao\git\akamai-tools\06_dig\bin\dig.py" 为例。
       通过vscode打开上面获取到的 PowerShell 配置文件, 添加以下内容并保存:

        ``` PowerShell
        function akdig {
            python.exe "C:\Users\shengjyerao\git\akamai-tools\06_dig\bin\dig.py" $args
        }
        ```

     3. 重新打开 PowerShell, 检查 dig 命令是否正常

        ``` PowerShell
        akdig -v
        ```

## 0x03. 功能菜单

| 参数           | 说明                                                                                            | 样例                                                 |
| :------------- | :---------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| h / help       | 显示帮助                                                                                        |                                                      |
| i / inputs     | 对 -i 之后的内容作为输入进行查询.                                                               | -i www.akamai.com                                    |
|                | 多个值之间以空格分隔.                                                                           | -i www.akamai.com www.akamai.cn                      |
| f / files      | 以文件作为输入进行查询.                                                                         | -f /Users/user/iptest-1.txt                          |
|                | 多个文件名之间以空格分隔.                                                                       | -f /Users/user/iptest-1.txt /Users/user/iptest-2.txt |
| o / output     | 输出格式, 支持 json/csv/txt                                                                     | -o csv                                               |
|                | 多个输出格式以空格分割.                                                                         | -o csv txt json                                      |
| t / type       | 查询记录类型. 默认为 A 记录.                                                                    | -t CNAME                                             |
| s / save       | 保存结果至文件. 当值为 h 时保存为与域名对应的文件, 其他值则为文件名.                            | -s h                                                 |
|                | 以 `-i www.akamai.com -t CNAME -o csv txt -s h` 为例, 输出文件为:                               |                                                      |
|                | www.akamai.com_CNAME.csv 和 www.akamai.com_CNAME.txt                                            |                                                      |
|                | 以 `-i www.akamai.com  www.akamai.cn -t CNAME -o csv txt -s 20231010_example` 为例, 输出文件为: | -s 20231010_example                                  |
|                | 20231010_example_CNAME.csv 和 20231010_example_CNAME.txt                                        |                                                      |
| d / dedulicate | 查询结果去重, 仅对 txt 格式输出有效.                                                            | -d                                                   |
| p / processing | 显示当前进度.                                                                                   | -p                                                   |
| e / exception  | 显示查询过程中的异常提示.                                                                       | -p                                                   |
| v / version    | 查看 dig 版本信息.                                                                              |                                                      |

## 0x04. 样例

- 查询域名
  - 输入:

    ``` shell
    akdig -i www.akamai.com www.akamai.com.cn
    ```

  - 输出:

    ``` shell

    ====> Result:
        {
        "json": {
            "www.akamai.com": {
                "127.0.0.1": {
                    "DNS": "127.0.0.1",
                    "Location": "Local",
                    "Provider": "Local ISP",
                    "Result": "Exception: The resolution lifetime expired after 1.104 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out."
                },
                "180.168.255.118": {
                    "DNS": "180.168.255.118",
                    "Location": "Shanghai, China",
                    "Provider": "ChinaNet",
                    "Result": "106.4.158.41"
                },
                "116.228.111.18": {
                    "DNS": "116.228.111.18",
                    "Location": "Shanghai, China",
                    "Provider": "ChinaNet",
                    "Result": "106.4.158.41"
                },
                "8.8.8.8": {
                    "DNS": "8.8.8.8",
                    "Location": "Mountain View CA, United States",
                    "Provider": "Google",
                    "Result": "61.147.221.40"
                }
            },
            "www.akamai.com.cn": {
                "127.0.0.1": {
                    "DNS": "127.0.0.1",
                    "Location": "Local",
                    "Provider": "Local ISP",
                    "Result": "Exception: The resolution lifetime expired after 1.105 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out."
                },
                "180.168.255.118": {
                    "DNS": "180.168.255.118",
                    "Location": "Shanghai, China",
                    "Provider": "ChinaNet",
                    "Result": "Exception: The DNS query name does not exist: www.akamai.com.cn."
                },
                "116.228.111.18": {
                    "DNS": "116.228.111.18",
                    "Location": "Shanghai, China",
                    "Provider": "ChinaNet",
                    "Result": "Exception: The DNS query name does not exist: www.akamai.com.cn."
                },
                "8.8.8.8": {
                    "DNS": "8.8.8.8",
                    "Location": "Mountain View CA, United States",
                    "Provider": "Google",
                    "Result": "Exception: The DNS query name does not exist: www.akamai.com.cn."
                }
            }
        }
    }
    ```

- 显示查询进度
  - 输入:

    ``` shell
    akdig -i www.akamai.com -p
    ```

  - 输出:

    ``` shell
    Working on hostname: www.akamai.com of DNS: 127.0.0.1, result: Exception: The resolution lifetime expired after 1.106 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out.
    Working on hostname: www.akamai.com of DNS: 180.168.255.118, result: 106.4.158.41
    Working on hostname: www.akamai.com of DNS: 116.228.111.18, result: 61.147.221.40
    Working on hostname: www.akamai.com of DNS: 8.8.8.8, result: 61.147.221.40

        ====> Result:
        {
        "json": {
            "www.akamai.com": {
                "127.0.0.1": {
                    "DNS": "127.0.0.1",
                    "Location": "Local",
                    "Provider": "Local ISP",
                    "Result": "Exception: The resolution lifetime expired after 1.106 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out."
                },
                "180.168.255.118": {
                    "DNS": "180.168.255.118",
                    "Location": "Shanghai, China",
                    "Provider": "ChinaNet",
                    "Result": "106.4.158.41"
                },
                "116.228.111.18": {
                    "DNS": "116.228.111.18",
                    "Location": "Shanghai, China",
                    "Provider": "ChinaNet",
                    "Result": "61.147.221.40"
                },
                "8.8.8.8": {
                    "DNS": "8.8.8.8",
                    "Location": "Mountain View CA, United States",
                    "Provider": "Google",
                    "Result": "61.147.221.40"
                }
            }
        }
    }
    ```

- csv, txt 输出:
  - 输入:

    ``` shell
    akdig -i www.akamai.com -o csv txt
    ```

  - 输出:

    ``` shell
        ====> Result:
        {
        "csv": {
            "www.akamai.com": [
                "DNS: 127.0.0.1, Location: Local, Provider: Local ISP, Result: Exception: The resolution lifetime expired after 1.103 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out.",
                "DNS: 180.168.255.118, Location: Shanghai, China, Provider: ChinaNet, Result: 106.4.158.41",
                "DNS: 116.228.111.18, Location: Shanghai, China, Provider: ChinaNet, Result: 106.4.158.41",
                "DNS: 8.8.8.8, Location: Mountain View CA, United States, Provider: Google, Result: 61.147.221.40"
            ]
        },
        "txt": {
            "www.akamai.com": "106.4.158.41, 106.4.158.41, 61.147.221.40, "
        }
    }
    ```

- txt 输出去重:
  - 输入:

    ``` shell
    akdig -i www.akamai.com -o txt -d
    ```

  - 输出:

    ``` shell

        ====> Result:
        {
        "txt": {
            "www.akamai.com": "106.4.158.41, 61.147.221.40, "
        }
    }
    ```

- txt 显示查询异常:
  - 输入:

    ``` shell
    akdig -i www.akamai.com -o txt -e
    ```

  - 输出:

    ``` shell
        ====> Result:
        {
        "txt": {
            "www.akamai.com": "Exception: The resolution lifetime expired after 1.104 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out., 106.4.158.41, 61.147.221.40, 61.147.221.40, "
        }
    }
    ```
