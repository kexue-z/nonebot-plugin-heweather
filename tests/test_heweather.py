import pytest
from nonebug import App

from .api import api_key, api_type


@pytest.mark.asyncio
async def test_heweather(app:App, monkeypatch: pytest.MonkeyPatch):
    from io import BytesIO

    import nonebot
    from PIL import Image
    from nonebot import get_driver
    from nonebot.adapters.onebot.v11 import Bot, Adapter, Message

    from nonebot_plugin_heweather.render_pic import render
    from nonebot_plugin_heweather.weather_data import (Weather,
                                                       CityNotFoundError)
    driver = get_driver()
    
    with monkeypatch.context() as m:
        async with (await app).test_server():  # type: ignore
            w_data = Weather(city_name='beijing', api_key=api_key, api_type=api_type)
            try:
                await w_data.load_data()
            except CityNotFoundError:
                pass
            
            img = await render(w_data)
            a = Image.open(BytesIO(img))
            a.save("weather.png", format="PNG")
