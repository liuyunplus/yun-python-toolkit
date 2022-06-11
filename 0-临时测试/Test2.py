import os

path = "/Users/dr.panda/Desktop/简历收集"
fileList = os.listdir(path)

for file_name in fileList:
    try:
        name, suffix = file_name.split(".")
        arr = name.split("-")
        if len(arr[2]) == 2:
            new_name = arr[0] + '-0' + arr[2] + '-' + arr[1]
        else:
            new_name = arr[0] + '-' + arr[2] + '-' + arr[1]
        new_name = new_name + "." + suffix
        old_name = file_name
        print(old_name, '->', new_name)
        os.rename(path + os.sep + old_name, path + os.sep + new_name)
    except:
        print("重命名失败：" + file_name)
