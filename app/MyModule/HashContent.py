import hashlib


def md5_content(content):
    m2 = hashlib.md5()
    m2.update(content.encode('utf-8'))
    return m2.hexdigest().upper()
