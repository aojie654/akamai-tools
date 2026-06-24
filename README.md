# Akamai Tools

THE REPO HAS ARCHIVED.

| Name        | Oversea                                             | China Mainland                                                 |
| ----------- | --------------------------------------------------- | -------------------------------------------------------------- |
| alias       | https://github.com/aojie654/akamai-tool-alias       | https://gl.aojie654.com:21043/aojie654/akamai-tool-alias       |
| cip         | https://github.com/aojie654/akamai-tool-cip         | https://gl.aojie654.com:21043/aojie654/akamai-tool-cip         |
| dig         | https://github.com/aojie654/akamai-tool-dig         | https://gl.aojie654.com:21043/aojie654/akamai-tool-dig         |
| ref decoder | https://github.com/aojie654/akamai-tool-ref-decoder | https://gl.aojie654.com:21043/aojie654/akamai-tool-ref-decoder |


## 0x01. Introduction

| No.  | Name                                                   | Status   | Description                                      |
| :--- | :----------------------------------------------------- | :------- | :----------------------------------------------- |
| 01   | [CIP](./01_cip/README.md)                              | Released | IP2Location with Akamai EdgeScape Pro            |
| 02   | Python Curl                                            | Canceled | simple curl with Akamai pragma headers in python |
| 03   | [Reference Decoder](./03_refference_decoder/README.md) | Released | decode the reference code with HTML encoded      |
| 04   | Timezone Convertor                                     | Released | Convert the timestamp with specific timezone     |
| 05   | [Bot Attacker](./05_bot_attacker/README.md)            | Released | Attack simulator                                 |
| 06   | [dig](./06_dig/README.md)                              | Released | DNS resolve with multple dns like dnschecker.org |

## 0x02. What shoud I do?

- Install [Python 3.8+](https://www.python.org/downloads/).
- (RECOMMENDED) Unix(linux/macOS) set the default shell to `zsh`.
  1. Check current shell you use:

     ``` shell
     echo ${SHELL}
     ```

     Output:

     ``` Text
     /bin/zsh
     ```

     Conguratulations! You are already using `zsh`, nothing need to do next.
     But if the output is not `zsh`, continue setting please.
  2. Run the command to change the default shell to `zsh`:

     ``` shell
     chsh -s /bin/zsh
     ```

  3. RESTART YOUR COMPUTER TO MAKE THE CHANGE EFFECT.
  4. Set variable `AK_TOOLS_HOME` for shell in ~/.zsh. For example, the repo is located at "/Users/sao/datas_l/git/akamai-tools" on my computer:

     ``` shell
     export AK_TOOLS_HOME="/Users/sao/datas_l/git/akamai-tools"
     ```

  5. Read the doc of the tool which you want to use.
