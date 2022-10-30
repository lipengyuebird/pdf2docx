# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/29 15:01
# @Author   : Perye(Li Pengyu)
# @FileName : generate_key.py
# @Software : PyCharm

import os
import pip

from constant import BASE_DIR

if __name__ == '__main__':
    try:
        import rsa
    except ImportError:
        pip.main(['install', 'rsa'])
    finally:
        import rsa

    (public_key, private_key) = rsa.newkeys(1024)

    if not os.path.exists(f'{BASE_DIR}rsa'):
        os.mkdir(f'{BASE_DIR}rsa')

    with open(f'{BASE_DIR}rsa/public.pem', 'wb+') as f:
        f.write(public_key.save_pkcs1())

    with open(f'{BASE_DIR}rsa/private.pem', 'wb+') as f:
        f.write(private_key.save_pkcs1())
