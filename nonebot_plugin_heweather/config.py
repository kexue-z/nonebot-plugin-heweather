from typing import Optional
from nonebot import get_driver
from pydantic import Extra, BaseModel

from .model import HourlyStyle, HourlyType


class Config(BaseModel, extra=Extra.ignore):
    qweather_apikey: Optional[str] = None
    qweather_apitype: Optional[str] = None
    qweather_hourlytype: Optional[HourlyType] = HourlyType.current_12h
    qweather_hourlystyle: Optional[HourlyStyle] = HourlyStyle.bar
    debug: bool = False


plugin_config = Config.parse_obj(get_driver().config)
QWEATHER_APIKEY = plugin_config.qweather_apikey
QWEATHER_APITYPE = plugin_config.qweather_apitype
QWEATHER_HOURLYTYPE = plugin_config.qweather_hourlytype
QWEATHER_HOURLYSTYLE = plugin_config.qweather_hourlystyle
DEBUG = plugin_config.debug
