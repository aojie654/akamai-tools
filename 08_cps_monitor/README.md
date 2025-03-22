# Akamai Tools: CPS Monitor

Get the pending enrollments list of Akamai CPS with Python libs `edgegrid-python, requests, pandas`.

[中文](./README_CN.md)

## 0x00. Introduction

- The commands are included in `command` area and text in green are notes.

``` shell
# All the text in this area are command like:
python3 --version

# But notes are started with #
```

## 0x01. Env

- Programing Language:
  - Python 3.8+
- Python Libs:
  - edgegrid-python
  - requests
  - pandas

## 0x02. How to install

1. Intall [Python 3.8+](https://www.python.org/downloads/).
   _**NOTES**_: The command Python3 maybe defferent which depends on the OS you are using. e.g. it's `python3` on Unix-like (Linux/MacOS, Unix for shortly) and `python` on Windoww. Be carefule to replace the command `python3` with `python`.
   Check the version of python:

    ``` shell
    python3 --version
    ```

    output:

    ``` Text
    Python 3.10.12
    ```

2. (Mainland China) Set up the mirror of python to speed up the libs installation.
    Use the following command to set mirrors as TUNA:

    ``` shell
    python3 -m pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple
    ```

3. Use the following command to install libs `edgegrid-python, requests, pandas`:

    ``` shell
    python3 -m pip install edgegrid-python requests pandas
    ```

4. Set up the config file:
   - Copy `08_cps_monitor/conf/conf.example.json` to `08_cps_monitor/conf/conf.json`
   - Example:

    ``` json
    {
        "log": {
            "level": 30
        },
        "api_client": {
            "section": "default"
        },
        "accounts": {
          "FC-1-1AAAA:1-AAAA": {
              "name": "Example Account",
              "users": [
                  "cdnadmin@example.com"
              ]
          },
        }
    }
    ```

    - log: (Dict/Object) Log config
      - level: (Int) Log level. Support INFO to ERROR. WARINING as default.
        - Referer: <https://docs.python.org/3/library/logging.html#levels>
    - api_client: (Dict/Object) Please sure about you are created a `.edgerc` file in home folder.
      - section: (String) The section of API Client in edgerc.
    - accounts: (Dict/Object) The accounts list which you want to list the erollments.
      - account_ask: (String) Will not user parameter: accountSwitchKey when calling CPS API, and will check the certificates in account which API Client located in.
        - name: (String) Account name without exactly match and only use for output.
        - users: (List/Array) User list. Can be use to send the script output to other platforms after integration with other tools.

5. Check the config correctly with command. E.g. the path of cps_monitor.py is `/Users/user/git/akamai-tools/08_cps_monitor/bin/cps_monitor.py`:

   ``` shell
   python3 /Users/user/git/akamai-tools/08_cps_monitor/bin/cps_monitor.py -h
   ```

   output:

   ``` text
    usage: Akamai CPS monitor [-h] [-a ACCOUNTS [ACCOUNTS ...]] [-u USERS [USERS ...]] [-c COMMAND] [-s] [-o] [-v]

    Monitoring Akamai CPS enrollments.

    options:
      -h, --help            show this help message and exit
      -a ACCOUNTS [ACCOUNTS ...], --accounts ACCOUNTS [ACCOUNTS ...]
                            Account switch keys and account name. Format: "ask^name". Default: None.
      -u USERS [USERS ...], --users USERS [USERS ...]
                            User IDs. Default: None.
      -c COMMAND, --command COMMAND
                            Values: [add|remove]. Default: add.
      -s, --slot            List enrolling slots. No command required.
      -o, --optimize        Optimize the accounts and user order in conf file. No command required.
      -v, --version         show program's version number and exit
   ```

6. Setup the alias:
   - Unix:
     Here is the settings on my mac:
     - The system variable of AK_TOOLS_HOME in shell means folder of repo.
     - Already set up the variable.
     - The path of cps_monitor if ${AK_TOOLS_HOME}/08_cps_monitor/bin/cps_monitor.py:
       1. Check the shell which you are using:

          ``` shell
          echo ${SHELL}
          ```

          Output:

          ``` Text
          /bin/zsh
          ```

       2. There are two options if your ourput like `/bin/bash`:

          - (Recommand) Change the default shell to `zsh`:
            - Run the command:

              ``` shell
              chsh -s /bin/zsh
              ```

            - Restart you compute to make change effect.
          - Set up alias in `~/.bashrc`. (May not work)

       3. I was added following lines to `~/.zshrc` for I'm using `zsh` and the source file is `~/.zshrc`:

          ``` shell
          # NOTE: Be sure about the variable is under the `export AK_TOOLS_HOME=....`
          alias akcm="python3 ${AK_TOOLS_HOME}/08_cps_monitor/bin/cps_monitor.py"
          ```

       4. Reopen the Terminal and check the alias works or not:

          ``` shell
          akcm -h
          ```

   - Windows
     1. Open your PowerShell and check the config file of it:

        ``` PowerShell
        echo $PROFILE
        ```

        Output:

        ``` Text
        C:\Users\shengjyerao\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
        ```

        the output is only let you know the path of the config of Powershell, and you need to create it manualy if it not exist.

     2. E.g. the path of cps_monitor.py is "C:\Users\shengjyerao\git\akamai-tools\08_cps_monitor\bin\cps_monitor.py". We can use vscode to open the file and add the following lines:

        ``` PowerShell
        function akcm {
            python.exe "C:\Users\shengjyerao\git\akamai-tools\08_cps_monitor\bin\cps_monitor.py" $args
        }
        ```

     3. Reopen the PowerShell, and check the alias works or not:

        ``` PowerShell
        akcm -v
        ```

7. (Optional) Set up the Webex Bot, then add webex_sender.py to contab.

## 0x03. Functions Menu

| args         | notes                                                                                                                        | simples                                                |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| h / help     | Display the help                                                                                                             | -h                                                     |
| c / command  | Options command. Accept: [add/remove]                                                                                        | -c add                                                 |
| a / accounts | Options target: accounts, the values are AccountSwitchKey which need use 'command' at same time.                             | -c add -a "1-AAAA\|Example.com"                        |
|              | Add: Split the accounts and AccountSwitchKey with "\|". (No exactly Account Name which only use to show the name in result). | -c add -a "1-AAAA\|Example.com" "1-AAAB\|Example2.com" |
|              | Remove: Only AccountSwitchKey needed.                                                                                        | -c remove -a "1-AAAA"                                  |
|              | Remeber to add quote " for values and split with space.                                                                      | -c remove -a "1-AAAA" "1-AAAB"                         |
| u / users    | (Developing) Options target: users, email as user id. Need to use with 'command' and 'account'.                              | -u "<admin@exmple.com>"                                |
|              | Remeber to add quote " for values and split with space.                                                                      | -u "<admin@exmple.com>"  "<cdnadmin@exmple.com>"       |
| s / slot     | Check the pending enrollments in account list.                                                                               | -s                                                     |
| o / optimize | Optimize the config file by account name.                                                                                    | -s                                                     |
| v / version  | Check the version.                                                                                                           | -v                                                     |

## 0x04. Simples

- Add accounts
  - input:

    ``` shell
    akcm -c add -a "1-AAAA|Example.com" "1-AAAB|Example2.com"
    ```

  - output:

    ``` shell

    ====> Result:
    Account: 1-AAAA|Example.com added.
    Account: 1-AAAB|Example2.com added.
    Config saved.
    Accounts: ['1-AAAA|Example.com', '1-AAAB|Example2.com'] processed.
    ```

- Remove accounts
  - input:

    ``` shell
    akcm -c remove -a "1-AAAA" "1-AAAB"
    ```

  - output:

    ``` shell

    ====> Result:
    Account: 1-AAAA|Example.com removed.
    Account: 1-AAAB|Example2.com removed.
    Config saved.
    Accounts: ['1-AAAA', '1-AAAB'] processed.
    ```

- List all the pending enrollments in account list
  - input:

    ``` shell
    akcm -s
    ```

  - output:

    ``` text
    init_log; Log folder:/opt/datas/git/akamai-tools/08_cps_monitor/log exist, create skipped.
    init_log; Log Path is: /opt/datas/git/akamai-tools/08_cps_monitor/log/cps_monitor_20240420.log
    processor_conf; Conf: /opt/datas/git/akamai-tools/08_cps_monitor/conf/conf.json loaded.
    init_edgerc; Conf: /home/user/.edgerc loaded, Api client section: default
    get_contracts; Add account with contracts: 1-AAAA|Example.com: ['1-C-AAAAA','1-C-AAAAB','1-C-AAAAC']
    get_slot_enrollments; No slots in contract: Example.com|1-C-AAAAA
    get_slot_enrollments; No pending changes in slot: 11111|www.example.com
    get_slot_expire; Slot expire: 111112|example.com|2024-05-30|39
    get_slot_enrollments; Add enrollment from contract: Example.com|1-C-AAAAB: 1111112|example.com|renewal|2024-05-30|39
    get_slot_enrollments; There is an exception:  get_slot_enrollments; 400: Example.com|1-C-AAAAC: ApiError(type=Forbidden, title=Invalid Contract, detail=The current contract does not belong to ACG list., source=Contract ID: 1-C-AAAAC)
    processor_slot; Slots processed: 1-AAAA|Example.com
    result_writer_slot; Output dir: /opt/datas/git/akamai-tools/08_cps_monitor/output exist, create skipped.
    result_writer_slot; Output JSON: /opt/datas/git/akamai-tools/08_cps_monitor/output/result_20240420.json, CSV: /opt/datas/git/akamai-tools/08_cps_monitor/output/result_20240420.csv.
    processor_slot; Slot processing end.
    ```

  - Check the pending enrollments in output file.
