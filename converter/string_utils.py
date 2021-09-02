import re


def snake_to_camel(string):
    """ 下划线转驼峰 """
    content = "".join(string.title().split("_"))
    return content[0].lower() + content[1:]


def snake_to_pascal(string):
    """ 下划线转首字母大写 """
    return "".join(string.title().split("_"))


def camel_to_snake(string):
    """ 驼峰转下滑线 """
    a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
    return a.sub(r'_\1', string).lower()