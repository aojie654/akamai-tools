#!/usr/local/bin/python3

import traceback

menu_json = {
    1: "curl",
    2: "openssl",
    3: "base64",
    4: "md5"
}

split_text = "="*20
menu_str = "{0}命令生成器{0}".format(split_text)
for key, value in menu_json.items():
    menu_str = "{}\n{}: {}".format(menu_str, key, value)
menu_str = "{0}\n{1}命令生成器{1}".format(menu_str, split_text)


while True:
    try:
        print(menu_str)
        menu_choice_str = input("请选择命令:")
        menu_choice_code = int(menu_choice_str)
        break
    except Exception:
        print(traceback.print_exc)

menu_choice = menu_json[menu_choice_code]
print(menu_choice)
