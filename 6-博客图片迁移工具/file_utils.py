
def replace(file, old_content, new_content):
    content = read_file(file)
    content = content.replace(old_content, new_content)
    rewrite_file(file, content)


def read_file(file):
    with open(file, encoding='UTF-8') as f:
        read_all = f.read()
        f.close()
    return read_all


def rewrite_file(file, data):
    with open(file, 'w', encoding='UTF-8') as f:
        f.write(data)
        f.close()


