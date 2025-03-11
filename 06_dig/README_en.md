# Akamai Tools: dig

Resolve the domains with multiple DNS with Python Lib: `dnspython`

[中文](./README.md)

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
  - dnspython

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

3. Install Python libs: dnspython:

    ``` shell
    python3 -m pip install dnspython
    ```

4. Update config file:
   1. Copy `06_dig/conf/dns.example.json` to `06_dig/conf/dns.json`
   2. (Optional) Update DNS server list
5. For e.g. the path `dig.py` is `/Users/user/git/akamai-tools/06_dig/bin/dig.py`, validate the `dig` works or not:

   ``` shell
   python3 /Users/user/git/akamai-tools/06_dig/bin/dig.py -i www.example.com
   ```

   Output:

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

6. Set up alias
   - Unix
     For example:
     - The shell variable of this repo is `AK_TOOLS_HOME`
     - Already setup the variable
     - The path of `dig` is `${AK_TOOLS_HOME}/06_dig/bin/dig.py`:
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
          alias akdig="python3 ${AK_TOOLS_HOME}/06_dig/bin/dig.py"
          ```

       4. Re-open the Terminal to check if the alias works:

          ``` shell
          akdig -v
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

     2. For example, the path of `dig` is "C:\Users\shengjyerao\git\akamai-tools\06_dig\bin\dig.py":
        Create a PowerShell config with following lines:

        ``` PowerShell
        function akdig {
            python.exe "C:\Users\shengjyerao\git\akamai-tools\06_dig\bin\dig.py" $args
        }
        ```

     3. Re-open PowerShell and check `dig` works or not:

        ``` PowerShell
        akdig -v
        ```

## 0x03. Menu

| Args               | Note                                                                                             | Example                                              |
| :----------------- | :----------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| No args / h / help | Display help                                                                                     |                                                      |
| i / inputs         | Lookup the arg(s) after -i                                                                       | -i www.akamai.com                                    |
|                    | Split with whitespace for multiple values.                                                       | -i www.akamai.com www.akamai.cn                      |
| f / files          | Lookup the content of file and add the result to it.                                             | -f /Users/user/iptest-1.txt                          |
|                    | Split with whitespace for multiple files.                                                        | -f /Users/user/iptest-1.txt /Users/user/iptest-2.txt |
| o / output         | Output format, support: json/csv/txt                                                             | -o csv                                               |
|                    | Split with whitespace for multiple format.                                                       | -o csv txt json                                      |
| t / type           | Records type. Default: A.                                                                        | -t CNAME                                             |
| s / save           | Save to file. Use domain as filename when value is: h, and other values as filename              | -s h                                                 |
|                    | For e.g. filename of `-i www.akamai.com -t CNAME -o csv txt -s h`:                               |                                                      |
|                    | `www.akamai.com_CNAME.csv` and `www.akamai.com_CNAME.txt`                                        |                                                      |
|                    | For e.g. filename of `-i www.akamai.com  www.akamai.cn -t CNAME -o csv txt -s 20231010_example`: | -s 20231010_example                                  |
|                    | `20231010_example_CNAME.csv` and `20231010_example_CNAME.txt`                                    |                                                      |
| d / dedulicate     | Remove the duplicated values. Only `txt` fromat support.                                         | -d                                                   |
| p / processing     | Display the processing.                                                                          | -p                                                   |
| e / exception      | Display the exceptions during processing                                                         | -p                                                   |
| v / version        | Check the version of `dig.py`                                                                    |                                                      |

## 0x04. Exmample

- Domain lookup
  - Input:

    ``` shell
    akdig -i www.akamai.com www.akamai.com.cn
    ```

  - Output:

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

- Display the processing
  - Input:

    ``` shell
    akdig -i www.akamai.com -p
    ```

  - Output:

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

- Format: `csv`, `txt`:
  - Input:

    ``` shell
    akdig -i www.akamai.com -o csv txt
    ```

  - Output:

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

- Remove duplicated values for format: `txt`:
  - Input:

    ``` shell
    akdig -i www.akamai.com -o txt -d
    ```

  - Output:

    ``` shell

        ====> Result:
        {
        "txt": {
            "www.akamai.com": "106.4.158.41, 61.147.221.40, "
        }
    }
    ```

- Display exceptions for format: `txt`:
  - Input:

    ``` shell
    akdig -i www.akamai.com -o txt -e
    ```

  - Output:

    ``` shell
        ====> Result:
        {
        "txt": {
            "www.akamai.com": "Exception: The resolution lifetime expired after 1.104 seconds: Server 127.0.0.1 UDP port 53 answered The DNS operation timed out., 106.4.158.41, 61.147.221.40, 61.147.221.40, "
        }
    }
    ```
