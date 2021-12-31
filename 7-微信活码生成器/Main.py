import qrcode

# 生成二维码
img = qrcode.make(data="https://gitee.com/liuyunplus/yun-image-repo/raw/master/temp/ED1C6E16CB104D7D88AF829DD916BEA0.jpg")
# 将二维码保存为图片
with open('test.png', 'wb') as f:
    img.save(f)