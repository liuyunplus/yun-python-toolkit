import os.path
import re
import shutil
import uuid
from common import FileUtils

BLOG_PATH = "blog_path"
BLOG_IMAGE_LIST = "blog_image_list"


def list_all_files(base_folder):
    """ 列出指定文件夹下的所有文件 """
    result_list = []
    for file_name in os.listdir(base_folder):
        file_path = os.path.join(base_folder, file_name)
        # 如果不是文件则跳过
        if not os.path.isfile(file_path):
            continue
        # 如果是隐藏文件也跳过
        if file_name.startswith("."):
            continue
        result_list.append(file_path)
    return result_list


def parse_blog_image(blog_path):
    """ 解析指定博客下的所有图片链接 """
    blog_content = open(blog_path, "r").read()
    image_list = []
    # 解析Markdown格式的图片链接
    md_image_list = re.findall("!\[.*?\]\((.*?)\)", blog_content)
    image_list.extend(md_image_list)
    # 解析Html格式的图片链接
    html_image_list = re.findall("<.*?img.*?src=\"(.*?)\"", blog_content)
    image_list.extend(html_image_list)
    return {
        BLOG_PATH: blog_path,
        BLOG_IMAGE_LIST: image_list
    }


def batch_parse_blog_image(base_folder):
    """ 批量解析博客的图片链接 """
    blog_path_list = list_all_files(base_folder)
    result_list = []
    for blog_path in blog_path_list:
        blog_image_info = parse_blog_image(blog_path)
        # 如果博客没有图片链接就跳过
        if not blog_image_info[BLOG_IMAGE_LIST]:
            continue
        result_list.append(blog_image_info)
    return result_list


def remove_and_replace(blog_folder, source_image_folder, target_image_folder):
    """ 移动图片 """
    blog_image_info_list = batch_parse_blog_image(blog_folder)
    for blog_image_info in blog_image_info_list:
        blog_path = blog_image_info[BLOG_PATH]
        for image_url in blog_image_info[BLOG_IMAGE_LIST]:
            # 获取旧的图片名称
            old_image_name = os.path.basename(image_url)
            old_image_path = source_image_folder + "/" + old_image_name
            if not os.path.exists(old_image_path):
                continue
            # 获取新的图片名称
            new_image_name = generate_image_name(old_image_name)
            new_image_path = target_image_folder + "/" + new_image_name
            # 移动图片到新路径并进行重命名
            shutil.copy(old_image_path, new_image_path)
            # 将博客中引用的图片进行替换
            FileUtils.replace(blog_path, image_url, "image/" + new_image_name)


def find_invalid_reference(blog_folder, image_folder):
    """
    找出博客上失效的图片引用(未在图片仓库中的引用就是失效引用)
    :param blog_folder:
    :param image_folder:
    :return:
    """
    repo_image_list = list_all_files(image_folder)
    blog_image_info_list = batch_parse_blog_image(blog_folder)
    for blog_image_info in blog_image_info_list:
        blog_path = blog_image_info[BLOG_PATH]
        # 遍历每篇博客的图片链接
        for image_url in blog_image_info[BLOG_IMAGE_LIST]:
            # 获取博客图片名称
            blog_image = os.path.basename(image_url)
            if blog_image not in repo_image_list:
                print("\033[31m博客:%s 图片:%s 不存在\033[0m" % (blog_path, blog_image))
            else:
                print("博客:%s 图片:%s 存在" % (blog_path, blog_image))


def find_redundant_image(blog_folder, image_folder):
    """
    找出图片仓库上冗余的图片(未被博客引用的图片就是冗余图片)
    :param blog_folder:
    :param image_folder:
    :return:
    """
    # 找出全部博客的图片
    blog_image_info_list = batch_parse_blog_image(blog_folder)
    blog_image_list = []
    for blog_image_info in blog_image_info_list:
        for image_url in blog_image_info[BLOG_IMAGE_LIST]:
            blog_image = os.path.basename(image_url)
            blog_image_list.append(blog_image)

    # 列出图片仓库的所有图片
    repo_image_list = list_all_files(image_folder)
    for repo_image in repo_image_list:
        if repo_image not in blog_image_list:
            print("\033[31m图片:%s 不存在\033[0m" % repo_image)
        else:
            print("图片:%s 存在" % repo_image)


def replace_image_prefix(blog_folder, image_prefix):
    """
    批量替换博客的图片链接前缀
    :param blog_folder:
    :param image_prefix:
    :return:
    """
    blog_image_info_list = batch_parse_blog_image(blog_folder)
    for blog_image_info in blog_image_info_list:
        blog_path = blog_image_info[BLOG_PATH]
        # 遍历每个博客的图片链接
        for old_image_url in blog_image_info[BLOG_IMAGE_LIST]:
            new_image_url = image_prefix + os.path.basename(old_image_url)
            FileUtils.replace(blog_path, old_image_url, new_image_url)


def generate_image_name(old_name):
    """ 生成新的图片名称(保留后缀) """
    new_name = str(uuid.uuid1()).replace("-", "")
    suffix = os.path.splitext(old_name)[-1]
    return new_name + suffix


blog_folder = "/Users/yliu2/Public/Github/yun-blog-builder/post"
image_prefix = "https://raw.githubusercontent.com/liuyunplus/yun-blog-builder/main/post/image/"
replace_image_prefix(blog_folder, image_prefix)

