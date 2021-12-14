import json
from common import StringUtils

class_name = "Activity"
jsonStr = """
{
  "activityId": 1,
  "activityName": "demoData",
  "activityType": "demoData",
  "groupId": 1,
  "creatorId": 1,
  "creatorName": "demoData",
  "applyStartTime": "2021/10/12, 5:29 下午",
  "applyEndTime": "2021/10/12, 5:29 下午",
  "activityStartTime": "2021/10/12, 5:29 下午",
  "activityEndTime": "2021/10/12, 5:29 下午",
  "activitySite": "demoData",
  "activityContent": "demoData",
  "limitNum": 1,
  "applicantsNum": 1,
  "activityStatus": 1,
  "canRegister": true,
  "canCancelRegister": true
}
"""


def build1(map):
    format_str = ""
    for key in map.keys():
        value = map[key]
        if isinstance(value, bool):
            format_str += "bool? _{};\n".format(key)
        elif isinstance(value, int):
            format_str += "int? _{};\n".format(key)
        elif isinstance(value, str):
            format_str += "String? _{};\n".format(key)
        elif isinstance(value, float):
            format_str += "double? _{};\n".format(key)
        elif isinstance(value, dict):
            format_str += "{0}? _{1};\n".format(StringUtils.camel_to_title(key), key)
        elif isinstance(value, list):
            format_str += "List<{0}>? _{1};\n".format(StringUtils.camel_to_title(key), key)
    return format_str.strip("\n")


def build2(map):
    str1 = ""
    str2 = ""
    for key in map.keys():
        value = map[key]
        if isinstance(value, bool):
            str1 += "bool? {},\n".format(key)
            str2 += "this._{0} = {0};\n".format(key)
        elif isinstance(value, int):
            str1 += "int? {},\n".format(key)
            str2 += "this._{0} = {0};\n".format(key)
        elif isinstance(value, str):
            str1 += "String? {},\n".format(key)
            str2 += "this._{0} = {0};\n".format(key)
        elif isinstance(value, float):
            str1 += "double? {},\n".format(key)
            str2 += "this._{0} = {0};\n".format(key)
        elif isinstance(value, dict):
            str1 += "{0}? {1},\n".format(StringUtils.camel_to_title(key), key)
            str2 += "this._{0} = {0};\n".format(key)
    str1 = str1.strip('\n')
    str1 = str1.strip(',')
    str2 = str2.strip('\n')
    format_str = """
{0}({{
{1}
}}) {{
{2}
}}
""".format(class_name, str1, str2)
    return format_str.strip("\n")


def build3(map):
    str1 = ""
    for key in map.keys():
        str1 += "{0}: map['{0}'],\n".format(key)
    str1 = str1.strip('\n')
    str1 = str1.strip(',')
    format_str = """
static {0} fromJson(Map<String, dynamic> map) {{
return {0}(
{1}
);
}}
""".format(class_name, str1)
    return format_str.strip("\n")


def build4(map):
    str1 = ""
    for key in map.keys():
        str1 += "map['{0}'] = this._{0};\n".format(key)
    str1 = str1.strip('\n')
    format_str = """
Map<String, dynamic> toJson() {{
Map<String, dynamic> map = {{}};
{0}
return map;
}}
""".format(str1)
    return format_str.strip("\n")


def build5(map):
    format_str = ""
    for key in map.keys():
        value = map[key]
        if isinstance(value, bool):
            format_str += "bool? get {0} => this._{0};\n".format(key)
        elif isinstance(value, int):
            format_str += "int? get {0} => this._{0};\n".format(key)
        elif isinstance(value, str):
            format_str += "String? get {0} => this._{0};\n".format(key)
        elif isinstance(value, float):
            format_str += "double? get {0} => this._{0};\n".format(key)
        elif isinstance(value, dict):
            format_str += "{0}? get {1} => this._{1};\n".format(StringUtils.camel_to_title(key), key)
    return format_str.strip("\n")


def build6(map):
    format_str = ""
    for key in map.keys():
        format_str += "set {0}(value) => this._{0} = value;\n".format(key)
    return format_str.strip("\n")


map = json.loads(jsonStr)
dart_str = """
class {0} {{

{1}

{2}

{3}

{4}

{5}

{6}

}}
""".format(class_name, build1(map), build2(map), build3(map), build4(map), build5(map), build6(map))
print(dart_str)
