import re

from nonebot import get_driver, on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.log import logger

from .get_weather import *
from .render_pic import render

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
    data = await get_city_weather(city)
    if type(data) is int:
        if data == 404:
            await weather.finish()
        else:
            await weather.finish(f"出错了! 错误代码={data}")
    img = await render(data) if data else None
    
    if get_driver().config.debug:
        debug_save_img(img)

    await weather.finish(MessageSegment.image(img))


def debug_save_img(img: bytes) -> None:
    from io import BytesIO
    from PIL import Image
    logger.debug("将会保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")
