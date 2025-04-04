from time import time

from jwt import encode

from .config import plugin_config
from .types import ConfigError


def get_jwt_token():
    if not (
        plugin_config.qweather_jwt_sub
        and plugin_config.qweather_jwt_kid
        and plugin_config.qweather_jwt_private_key
    ):
        raise ConfigError(
            "请检查是否遗漏了 QWEATHER_JWT_SUB "
            "QWEATHER_JWT_KID QWEATHER_JWT_PRIVATE_KEY "
            "中的其中一项"
        )

    payload = {
        "iat": int(time()) - 30,
        "exp": int(time()) + 900,
        "sub": plugin_config.qweather_jwt_sub,
    }
    headers = {
        "kid": plugin_config.qweather_jwt_kid,
        "alg": "EdDSA",
    }

    encoded_jwt = encode(
        payload,
        key=plugin_config.qweather_jwt_private_key,
        algorithm="EdDSA",
        headers=headers,
    )
    return encoded_jwt
