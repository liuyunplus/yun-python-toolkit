
def replace(file, old_content, new_content):
    """替换文件内容"""
    content = read_file(file)
    content = content.replace(old_content, new_content)
    rewrite_file(file, content)


def read_file(file):
    """读取文件"""
    with open(file, encoding='UTF-8') as f:
        read_all = f.read()
        f.close()
    return read_all


def rewrite_file(file, data):
    """覆写文件"""
    with open(file, 'w', encoding='UTF-8') as f:
        f.write(data)
        f.close()


