# Reference Error String Decoder

## 0x00. How it works

1. Remove the string: "Reference\&\#32;\&\#35;" in Reference String ("Reference #" in HTML encoded)
2. Replace "\&\#46;" to "."

## 0x01. How to use

1. create an alias in shell rc/profile:

    ``` shell
    alias akrefd="python3 ${AK_TOOLS_HOME}/03_refference_decoder/bin/reffer_decoder.py"
    ```

2. Using alias "reftrans" but remember to add the double quote to reference code like:

    ``` shell
    akrefd "Reference&#32;&#35;9&#46;99093e17&#46;1655882606&#46;13d27567"
    ```

    then output will like to:

    ``` shell
    9.99093e17.1655882606.13d27567
    ```
