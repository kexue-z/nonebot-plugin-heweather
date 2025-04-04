from time import time

from jwt import encode

from .config import (
    QWEATHER_JWT_KID,
    QWEATHER_JWT_PRIVATE_KEY,
    QWEATHER_JWT_SUB,
)


def get_jwt_token():
    payload = {
        "iat": int(time()) - 30,
        "exp": int(time()) + 900,
        "sub": QWEATHER_JWT_SUB or "",
    }
    headers = {
        "kid": QWEATHER_JWT_KID,
        "alg": "EdDSA",
    }

    encoded_jwt = encode(
        payload,
        QWEATHER_JWT_PRIVATE_KEY or "",
        algorithm="EdDSA",
        headers=headers,
    )
    return encoded_jwt
