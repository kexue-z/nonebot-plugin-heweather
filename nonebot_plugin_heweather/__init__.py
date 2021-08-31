from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message, MessageSegment
import base64
from .get_weather import *
from .convrt_pic import *
from io import BytesIO

weather = on_command("天气", priority=1)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


@weather.handle()
async def _(bot: Bot, event: MessageEvent):
    city = str(event.get_message())
    if city:
        try:
            data = await get_City_Weather(city)
        except KeyError:
            await weather.finish("这个地方不在天气数据库中哦 >_<")
        img = draw(data)
        b64 = img_to_b64(img)
        await weather.finish(MessageSegment.image(b64))
    else:
        await weather.finish("地点是...空气吗?? >_<")
