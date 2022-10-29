# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/28 22:59
# @Author   : Perye(Li Pengyu)
# @FileName : user_service.py
# @Software : PyCharm
import time
import uuid
from typing import Optional

from authlib.jose import jwt, JWTClaims
from authlib.jose.errors import *

header = {'alg': 'RS256', "typ": "JWT"}
with open('private_key.pem') as f:
    private_key = f.read()
with open('public_key.pem') as f:
    public_key = f.read()


def generate_user_id() -> str:
    """
    return a user ID by UUID1
    """
    return uuid.uuid1().hex


def encrypt_token(user_id: str) -> str:
    """
    generate a token by user ID
    :param user_id: user ID
    :return token
    """
    return 'Bearer ' + jwt.encode(header, {
        'iss': 'Perye',
        'sub': user_id,
        'exp': int(time.time()) + 1000 * 60 * 60 * 24 * 7,
        'iat': int(time.time())
    }, private_key)


def decrypt_token(token: str) -> Optional[str]:
    """
    validate the token and get the user ID of a token
    :param token: token
    :return user ID
    """
    if not token:
        return None
    try:
        claims = jwt.decode(token.split('Bearer ')[0], public_key)
        claims.validate()
        return claims.get('sub')
    except BadSignatureError:
        return None
    except InvalidClaimError:
        return None


def renewed_header(user_id: str):
    return [('Authorization', 'Bearer ' + encrypt_token(user_id))]