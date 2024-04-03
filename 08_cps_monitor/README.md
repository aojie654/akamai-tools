# Akamai Tools: CPS Monitor

使用 Python 库 `edgegrid-python, requests` 获取 CPS 证书 enroll 状态

[English Doc](./README_en.md)

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
  - edgegrid-python
  - requests

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

3. 通过以下命令，为 Python 安装第三方库 edgegrid-python, requests:

    ``` shell
    python3 -m pip install edgegrid-python requests
    ```

4. 修改配置文件:
   - 复制 `08_cps_monitor/conf/conf.example.json` 为 `08_cps_monitor/conf/conf.json`
   - 样例:

    ``` json
    {
        "api_client": {
            "section": "default"
        },
        "accounts": {
        }
    }
    ```

    - api_client: 请确保在 home 目录下正确存放了 .edgerc 文件
      - section: edgerc 中需要使用的 API Client 所在的 section.

5. 以 cps_monitor.py 路径为 `/Users/user/git/akamai-tools/08_cps_monitor/bin/cps_monitor.py` 为例, 通过以下命令查看 dig 是否运行正常:

   ``` shell
   python3 /Users/user/git/akamai-tools/08_cps_monitor/bin/cps_monitor.py -h
   ```

   输出:

   ``` shell
    usage: cps_monitor.py [-h] [-a ACCOUNTS [ACCOUNTS ...]] [-u USERS [USERS ...]] [-c COMMAND] [-s]

    Akamai CPS monitor.

    options:
    -h, --help            show this help message and exit
    -a ACCOUNTS [ACCOUNTS ...], --accounts ACCOUNTS [ACCOUNTS ...]
                            Account switch keys and account name. Format: "ask|name". Default: None.
    -u USERS [USERS ...], --users USERS [USERS ...]
                            User IDs. Default: None.
    -c COMMAND, --command COMMAND
                            Values: [add|remove]. Default: add.
    -s, --slot            List enrolling slots. No command required.
   ```

6. 设置 alias
   - Unix
     以我的环境为例:
     - repo 对应 Shell 变量为 AK_TOOLS_HOME
     - 已经设置过该变量
     - dig 文件的路径是 ${AK_TOOLS_HOME}/08_cps_monitor/bin/cps_monitor.py:
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
          alias akcm="python3 ${AK_TOOLS_HOME}/08_cps_monitor/bin/cps_monitor.py"
          ```

       4. 重新打开 Terminal, 进行一次帮助检查配置是否正确:

          ``` shell
          akcm -h
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

     2. 以文件路径 "C:\Users\shengjyerao\git\akamai-tools\08_cps_monitor\bin\cps_monitor.py" 为例。
       通过vscode打开上面获取到的 PowerShell 配置文件, 添加以下内容并保存:

        ``` PowerShell
        function akcm {
            python.exe "C:\Users\shengjyerao\git\akamai-tools\08_cps_monitor\bin\cps_monitor.py" $args
        }
        ```

     3. 重新打开 PowerShell, 检查 dig 命令是否正常

        ``` PowerShell
        akcm -v
        ```

## 0x03. 功能菜单

| 参数         | 说明                                                                                                  | 样例                                                   |
| :----------- | :---------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| h / help     | 显示帮助                                                                                              | -h                                                     |
| c / command  | 操作命令, 可用值: [add/remove]                                                                        | -c add                                                 |
| a / accounts | 操作对象为 accounts, account 为 AccountSwitchKey 需搭配 command 使用.                                 | -c add -a "1-AAAA\|Example.com"                        |
|              | 添加 accounts 时以 "\|" 分割 AccountSwitchKey 和 account 名称(无需准确 Account Name, 仅用作输出标识). | -c add -a "1-AAAA\|Example.com" "1-AAAB\|Example2.com" |
|              | 移除 accounts 时仅需输入 AccountSwitchKey.                                                            | -c remove -a "1-AAAA"                                  |
|              | 多个值之间以空格分隔, 建议添加引号.                                                                   | -c remove -a "1-AAAA" "1-AAAB"                         |
| u / users    | (未完成) 操作对象为 users, user 为邮箱地址, 需搭配 command 和 account 使用.                           | -u "<admin@exmple.com>"                                  |
|              | 多个文件名之间以空格分隔, 建议添加引号.                                                               | -u "<admin@exmple.com>"  "<cdnadmin@exmple.com>"           |
| s / slot     | 查询配置中所有 account 正在 enroll 的证书                                                             | -s                                                     |

## 0x04. 样例

- 添加 accounts
  - 输入:

    ``` shell
    akcm -c add -a "1-AAAA|Example.com" "1-AAAB|Example2.com"
    ```

  - 输出:

    ``` shell

    ====> Result:
    Account: 1-AAAA|Example.com added.
    Account: 1-AAAB|Example2.com added.
    Config saved.
    Accounts: ['1-AAAA|Example.com', '1-AAAB|Example2.com'] processed.
    ```

- 移除 accounts
  - 输入:

    ``` shell
    akcm -c remove -a "1-AAAA" "1-AAAB"
    ```

  - 输出:

    ``` shell

    ====> Result:
    Account: 1-AAAA|Example.com removed.
    Account: 1-AAAB|Example2.com removed.
    Config saved.
    Accounts: ['1-AAAA', '1-AAAB'] processed.
    ```

- 列出在 enroll 状态的证书
  - 输入:

    ``` shell
    akcm -s
    ```

  - 输出:

    ``` shell

    ====> Result:
    Log Path is: /Users/user/git/akamai-tools/08_cps_monitor/log/cps_monitor_20240331.log
    Config loaded.
    Config: /Users/user/.edgerc loaded, Api client section: aaa.
    Add account: 1-AAAA with contracts: ['1-AAAA']
    400: ApiError(type=Forbidden, title=Invalid Contract, detail=The current contract does not belong to ACG list., source=Contract ID: 1-AAAA)
    Add account: 1-AAAB with contracts: ['1-AAABA', '1-AAABB']
    No enrollments in contract: Example2.com > 1-AAAB
    Add enrollment: {'Account Name': 'Example2.com', 'Account Switch Key': '1-AAAB', 'Contract': '1-AAABB', 'Common Name': 'example.com', 'Slot ID': 111111}
    Slots processed.
    Output: CSV: /Users/user/git/akamai-tools/08_cps_monitor/output/result_20240331.csv.
    ```

  - 检查输出文件 查看 enroll 的证书列表
