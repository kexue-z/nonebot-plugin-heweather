import base64
import re
from io import BytesIO

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, Message, MessageEvent, MessageSegment

from .convrt_pic import *
from .get_weather import *

weather = on_regex(r".*?(.*)天气.*?", priority=1)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


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
    img = draw(data) if data else None
    b64 = img_to_b64(img) if img else None
    if data["warning"]:
        warning = data["warning"]["warning"]
        text = ""
        for i in range(len(warning)):
            text = f'\n{warning[i]["text"]}'
        await weather.finish(MessageSegment.image(b64) + MessageSegment.text(text))
    else:
        await weather.finish(MessageSegment.image(b64))
