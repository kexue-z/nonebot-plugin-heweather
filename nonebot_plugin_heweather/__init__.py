from nonebot import on_keyword
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from .render_pic import render
from .weather_data import Weather, ConfigError, CityNotFoundError
from .config import DEBUG, QWEATHER_APIKEY, QWEATHER_APITYPE, Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-heweather",
    description="和风天气图片显示插件",
    usage="天气地名 / 地名天气",
    type="application",
    homepage="https://github.com/kexue-z/nonebot-plugin-heweather",
    config=Config,
    extra={},
    supported_adapters={"~onebot.v11"},
)


if DEBUG:
    logger.debug("将会保存图片到 weather.png")


weather = on_keyword({"天气"}, priority=1)


@weather.handle()
async def _(matcher: Matcher, event: MessageEvent):
    if not (QWEATHER_APIKEY and QWEATHER_APITYPE):
        raise ConfigError("请设置 qweather_apikey 和 qweather_apitype")

    city = ""
    if args := event.get_plaintext().split("天气"):
        city = args[0].strip() or args[1].strip()
        if not city:
            await weather.finish("地点是...空气吗?? >_<")

        # 判断指令前后是否都有内容，如果是则结束，否则跳过。
        if (args[0].strip() == "") == (args[1].strip() == ""):
            await weather.finish()
    w_data = Weather(city_name=city, api_key=QWEATHER_APIKEY, api_type=QWEATHER_APITYPE)
    try:
        await w_data.load_data()
    except CityNotFoundError:
        matcher.block = False
        await weather.finish()

    img = await render(w_data)

    if DEBUG:
        debug_save_img(img)

    await weather.finish(MessageSegment.image(img))


def debug_save_img(img: bytes) -> None:
    from io import BytesIO

    from PIL import Image

    logger.debug("保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")
