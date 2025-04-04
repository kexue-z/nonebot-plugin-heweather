from nonebot import get_driver
from nonebug import App
import pytest


@pytest.mark.asyncio
async def test_heweather(app: App):
    from io import BytesIO

    from PIL import Image

    from nonebot_plugin_heweather.render_pic import render
    from nonebot_plugin_heweather.weather_data import CityNotFoundError, Weather

    async with app.test_server():
        config = get_driver().config
        api_key = config.qweather_apikey
        api_type = int(config.qweather_apitype)
        w_data = Weather(city_name="beijing", api_key=api_key, api_type=api_type)
        try:
            await w_data.load_data()
        except CityNotFoundError:
            pass

        img = await render(w_data)
        a = Image.open(BytesIO(img))
        a.save("docs/weather.png", format="PNG")
