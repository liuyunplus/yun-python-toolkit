import hashlib


# 加密方法
def encrypt(content):
    new_md5 = hashlib.md5()
    new_md5.update(content.encode(encoding='utf-8'))
    return new_md5.hexdigest()
