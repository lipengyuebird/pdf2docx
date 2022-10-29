# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/29 15:01
# @Author   : Perye(Li Pengyu)
# @FileName : generate_key.py
# @Software : PyCharm
import pip

if __name__ == '__main__':
    try:
        import rsa
    except ImportError:
        pip.main(['install', 'rsa'])
    finally:
        import rsa

    (public_key, private_key) = rsa.newkeys(1024)

    with open('public.pem', 'wb+') as f:
        f.write(public_key.save_pkcs1())

    with open('private.pem', 'wb+') as f:
        f.write(private_key.save_pkcs1())
