# Akamai Tools

## 0x01. Introduction

| No.  | Name                                                   | Processing | Description                                      |
| :--- | :----------------------------------------------------- | :--------- | :----------------------------------------------- |
| 01   | [cip](./01_cip/README.md)                              | v0.2.0     | IP2Location with Akamai EdgeScape Pro            |
| 02   | python_curl                                            | 暂时鸽了   | simple curl with Akamai pragma headers in python |
| 03   | [reference_decoder](./03_refference_decoder/README.md) | Finished   | decode the reference code with HTML encoded      |
| 04   | timezone_convertor                                     | developing | Convert the timestamp with specific timezone     |

## 0x02. What shoud I do?

- Install [Python 3.8+](https://www.python.org/downloads/).
- (RECOMMENDED) Unix(linux/macOS) set the default shell to `zsh`.
  1. Check current shell you use:

     ``` Bash
     echo ${SHELL}
     ```

     Output:

     ``` Text
     /bin/zsh
     ```

     Conguratulations! You are already using `zsh`, nothing need to do next.
     But if the output is not `zsh`, continue setting please.
  2. Run the command to change the default shell to `zsh`:

     ``` Bash
     chsh -s /bin/zsh
     ```

  3. RESTART YOUR COMPUTER TO MAKE THE CHANGE EFFECT.
