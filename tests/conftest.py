import pytest
from nonebug.app import App

from .api import api_key, api_type


@pytest.fixture
async def app(
    nonebug_init: None,
    monkeypatch: pytest.MonkeyPatch,
) -> App:
    import nonebot

    config = nonebot.get_driver().config

    config.qweather_apikey = api_key
    config.qweather_apitype = api_type

    # 加载插件
    nonebot.load_plugin("nonebot_plugin_heweather")

    return App(monkeypatch)
