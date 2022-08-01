# Akamai Tools

## 0x01. Introduction

| No.  | Name                                                   | Processing | Description                                      |
| :--- | :----------------------------------------------------- | :--------- | :----------------------------------------------- |
| 01   | [CIP](./01_cip/README.md)                              | developing | IP2Location with Akamai EdgeScape Pro            |
| 02   | Python Curl                                            | 暂时鸽了   | simple curl with Akamai pragma headers in python |
| 03   | [Reference Decoder](./03_refference_decoder/README.md) | Finished   | decode the reference code with HTML encoded      |
| 04   | Timezone Convertor                                     | developing | Convert the timestamp with specific timezone     |
| 05   | [Bot Attacker](./05_bot_attacker/README.md)            | developing | Attack simulator                                 |

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
  4. Set variable for shell in ~/.zsh:

     ``` Bash
     export AK_TOOLS_HOME="/Users/sao/datas_l/git/akamai-tools"
     ```

  5. Read the doc of the tool which you want to use.
