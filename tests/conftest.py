from os import getenv

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
import pytest


@pytest.fixture(scope="session", autouse=True)
def _():
    # 加载适配器
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    config = nonebot.get_driver().config

    config.qweather_apikey = getenv("QWEATHER_APIKEY")
    config.qweather_apitype = getenv("QWEATHER_APITYPE")
    config.qweather_forecase_days = getenv("QWEATHER_FORECASE_DAYS")

    # 加载插件
    nonebot.load_plugin("nonebot_plugin_heweather")
