from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

'''
AES对称加密算法
'''


# 补位成16的倍数
def pad_to_16(value):
    return pad(value.encode(), 16)


# 加密方法
def encrypt(text, key):
    aes = AES.new(pad_to_16(key), AES.MODE_ECB)
    encrypted_aes = aes.encrypt(pad_to_16(text))
    encrypted_text = str(base64.encodebytes(encrypted_aes), encoding='utf-8')
    return encrypted_text


# 解密方法
def decrypt(text, key):
    aes = AES.new(pad_to_16(key), AES.MODE_ECB)
    decrypted_base64 = base64.decodebytes(text.encode(encoding='utf-8'))
    decrypted_aes = aes.decrypt(decrypted_base64)
    unpad_aes = unpad(decrypted_aes, 16)
    decrypted_text = str(unpad_aes, encoding='utf-8').strip()
    return decrypted_text