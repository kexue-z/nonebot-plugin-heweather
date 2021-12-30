import re

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment

from .render_pic import render
from .get_weather import *

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
    data = await get_City_Weather(city)
    if type(data) is int:
        if data == 404:
            await weather.finish()
        else:
            await weather.finish(f"出错了! 错误代码={data}")
    img = await render(data) if data else None

    # from PIL import Image
    # import io

    # a = Image.open(io.BytesIO(img))
    # a.save("template2pic.png", format="PNG")

    await weather.finish(MessageSegment.image(img))
