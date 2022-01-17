import re

from nonebot import get_driver, on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.log import logger

from .weather_data import Weather
from .render_pic import render

api_key = get_driver().config.qweather_apikey
api_type = get_driver().config.qweather_apitype

weather = on_regex(r".*?(.*)天气.*?", priority=1)


def get_msg(msg) -> str:
    msg1 = re.search(r".*?(.*)天气.*?", msg)
    msg2 = re.search(r".*?天气(.*).*?", msg)
    msg1 = msg1.group(1).replace(" ", "")
    msg2 = msg2.group(1).replace(" ", "")
    msg = msg1 if msg1 else msg2

    return msg


@weather.handle()
async def _(bot: Bot, event: MessageEvent):
    city = get_msg(event.get_plaintext())
    if city is None:
        await weather.finish("地点是...空气吗?? >_<")

    w_data = Weather(city_name=city, api_key=api_key, api_type=api_type)
    await w_data.load_data()

    img = await render(w_data)

    if get_driver().config.debug:
        debug_save_img(img)

    await weather.finish(MessageSegment.image(img))


def debug_save_img(img: bytes) -> None:
    from io import BytesIO
    from PIL import Image

    logger.debug("将会保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")
