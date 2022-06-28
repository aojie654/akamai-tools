# encoding = utf-8

import sys

# sys.argv = [__file__, "Reference&#32;&#35;9&#46;77cc4d17&#46;1655700986&#46;131e60fa"]

help_text = """
1. 使用方法:
    python3 reffer_translation.py "HTML_Encoded_Error_String"
    注: HTML_Encoded_Error_String 两侧需要双引号.
    例如:
    1. 输入:
        python3 reffer_translation.py Reference&#32;&#35;9&#46;77cc4d17&#46;1655700986&#46;131e60fa
    2. 输出:
        9.77cc4d17.1655700986.131e60fa
"""

if len(sys.argv) < 2 :
    print()
refer_string_html = sys.argv[1]
# 去除开头
refer_string = refer_string_html.replace("Reference&#32;&#35;", "").replace("&#46;", ".")

print(refer_string)
