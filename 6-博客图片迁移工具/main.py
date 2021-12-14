import os.path
import re
import shutil
import uuid
from common import FileUtils


def list_all_files(base_folder):
    file_names = []
    for file_name in os.listdir(base_folder):
        if not os.path.isfile(os.path.join(base_folder, file_name)):
            continue
        if file_name.startswith("."):
            continue
        file_names.append(file_name)
    return file_names


def get_blog_image_map(blog_name):
    blog_file = open(os.path.join(blog_folder, blog_name), "r")
    blog_content = blog_file.read()
    image_url_list = []
    list1 = re.findall("!\[.*?\]\((.*?)\)", blog_content)
    image_url_list.extend(list1)
    list2 = re.findall("<.*?img.*?src=\"(.*?)\"", blog_content)
    image_url_list.extend(list2)
    result = {
        "blogName": blog_name,
        "imageList": image_url_list
    }
    return result


def list_all_blog_image(blog_folder):
    blog_name_list = list_all_files(blog_folder)
    blog_image_list = []
    for blog_name in blog_name_list:
        blog_image_map = get_blog_image_map(blog_name)
        if not blog_image_map["imageList"]:
            continue
        blog_image_list.append(blog_image_map)
    return blog_image_list


def get_new_image_path(old_name):
    new_name = str(uuid.uuid1()).replace("-", "")
    suffix = os.path.splitext(old_name)[-1]
    return target_image_folder + "/" + new_name + suffix


def remove_and_replace():
    blog_image_map_list = list_all_blog_image(blog_folder)
    for blog_image_map in blog_image_map_list:
        blog_name = blog_image_map["blogName"]
        for image_url in blog_image_map["imageList"]:
            old_image_name = os.path.basename(image_url)
            old_image_path = source_image_folder + "/" + blog_name.replace(".md", "") + "/" + old_image_name
            if not os.path.exists(old_image_path):
                continue
            new_image_path = get_new_image_path(old_image_name)

            # 移动并重命名图片
            print(old_image_path, new_image_path)
            shutil.copy(old_image_path, new_image_path)

            # 替换文件图片链接
            new_image_name = os.path.basename(new_image_path)
            print(blog_folder + "/" + blog_name, image_url, "image/" + new_image_name)
            FileUtils.replace(blog_folder + "/" + blog_name, image_url, "image/" + new_image_name)


def scan_blog_image():
    # 列出图片仓库的所有图片
    image_list = list_all_files(target_image_folder)
    # 搜索博客文章的所有图片
    blog_image_map_list = list_all_blog_image(blog_folder)
    for blog_image_map in blog_image_map_list:
        blog_name = blog_image_map["blogName"]
        # 遍历每篇博客的图片链接
        for image_url in blog_image_map["imageList"]:
            # 获取博客图片名称
            blog_image = os.path.basename(image_url)
            if blog_image not in image_list:
                print("\033[31m博客:%s 图片:%s 不存在\033[0m" % (blog_name, blog_image))
            else:
                print("博客:%s 图片:%s 存在" % (blog_name, blog_image))


def scan_image_repo():
    # 获取博客的所有图片
    blog_image_map_list = list_all_blog_image(blog_folder)
    blog_images = []
    for blog_image_map in blog_image_map_list:
        for image_url in blog_image_map["imageList"]:
            blog_image = os.path.basename(image_url)
            blog_images.append(blog_image)

    # 列出图片仓库的所有图片
    image_list = list_all_files(target_image_folder)
    for image in image_list:
        if image not in blog_images:
            print("\033[31m图片:%s 不存在\033[0m" % image)
        else:
            print("图片:%s 存在" % image)


blog_folder = "/Users/yliu2/Public/Github/yun-blog/source/_posts"
source_image_folder = "/Users/yliu2/Public/Github/yun-blog-image"
target_image_folder = "/Users/yliu2/Public/Github/yun-blog/source/_posts/image"
scan_image_repo()
