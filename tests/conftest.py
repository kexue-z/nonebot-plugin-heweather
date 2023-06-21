import pytest
import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from .api import api_key, api_type


@pytest.fixture(scope="session", autouse=True)
def load_bot():
    # 加载适配器
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    config = nonebot.get_driver().config

    config.qweather_apikey = api_key
    config.qweather_apitype = api_type

    # 加载插件
    nonebot.load_plugin("nonebot_plugin_heweather")
