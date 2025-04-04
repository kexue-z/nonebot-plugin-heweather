from nonebot.plugin import get_plugin_config
from pydantic import BaseModel, Field

from .model import HourlyType


class Config(BaseModel):
    qweather_apihost: str = Field(default="https://api.qweather.com")
    qweather_apikey: str | None = Field(
        default=None, deprecated="建议使用更安全的JWT key"
    )
    qweather_apitype: int | None = Field(default=None)
    qweather_hourlytype: HourlyType | None = Field(default=HourlyType.current_12h)
    qweather_forecase_days: int | None = Field(default=3)
    qweather_use_jwt: bool | None = Field(
        default=True, description="是否使用 JWT，默认 True"
    )
    qweather_jwt_sub: str | None = Field(
        default=None, description="JWT sub，即控制台中的项目ID"
    )
    qweather_jwt_private_key: str | None = Field(
        default=None, deprecated="JWT 私钥文本，需要自行生成"
    )

    qweather_jwt_kid: str | None = Field(
        default=None, description="JWT Key ID，即控制台中上传公钥后即可获取"
    )
    debug: bool | None = Field(default=False)


plugin_config: Config = get_plugin_config(Config)
QWEATHER_APIHOST = plugin_config.qweather_apihost
QWEATHER_APIKEY = plugin_config.qweather_apikey
QWEATHER_APITYPE = plugin_config.qweather_apitype
QWEATHER_HOURLYTYPE = plugin_config.qweather_hourlytype
QWEATHER_FORECASE_DAYS = plugin_config.qweather_forecase_days
DEBUG = plugin_config.debug
QWEATHER_USE_JWT = plugin_config.qweather_use_jwt
QWEATHER_JWT_SUB = plugin_config.qweather_jwt_sub
QWEATHER_JWT_PRIVATE_KEY = plugin_config.qweather_jwt_private_key
QWEATHER_JWT_KID = plugin_config.qweather_jwt_kid
