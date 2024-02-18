from nonebot import get_plugin_config
from pydantic import BaseModel, Field

from .model import HourlyType


class Config(BaseModel):
    qweather_apikey: str = Field(default=None)
    qweather_apitype: str = Field(default=None)
    qweather_hourlytype: HourlyType = Field(default=HourlyType.current_12h)
    qweather_forecase_days: int = Field(default=3)
    debug: bool = Field(default=False)


plugin_config: Config = get_plugin_config(Config)
QWEATHER_APIKEY = plugin_config.qweather_apikey
QWEATHER_APITYPE = plugin_config.qweather_apitype
QWEATHER_HOURLYTYPE = plugin_config.qweather_hourlytype
QWEATHER_FORECASE_DAYS = plugin_config.qweather_forecase_days
DEBUG = plugin_config.debug
