from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")

from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna

from .config import Config, plugin_config
from .render_pic import render
from .weather_data import CityNotFoundError, ConfigError, Weather

__plugin_meta__ = PluginMetadata(
    name="和风天气",
    description="和风天气图片显示插件",
    usage="天气地名 / 地名天气",
    type="application",
    homepage="https://github.com/kexue-z/nonebot-plugin-heweather",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)


if plugin_config.debug:
    logger.debug("将会保存图片到 weather.png")


weather = on_alconna(Alconna("天气", Args["city", str]), block=True, priority=1)
weather.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
weather.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})


@weather.handle()
async def _(matcher: Matcher, city: str):
    if not (plugin_config.qweather_apikey or plugin_config.qweather_use_jwt):
        raise ConfigError("请设置 QWEATHER_APIKEY 或 JWT ")

    if plugin_config.qweather_apitype is None:
        raise ConfigError("请设置 QWEATHER_APITYPE")

    w_data = Weather(city_name=city, api_type=plugin_config.qweather_apitype)
    try:
        await w_data.load_data()
    except CityNotFoundError:
        logger.warning(f"找不到城市: {city}")
        matcher.block = False
        await matcher.finish()

    img = await render(w_data)

    if plugin_config.debug:
        debug_save_img(img)

    await UniMessage.image(raw=img).send()


def debug_save_img(img: bytes) -> None:
    from io import BytesIO

    from PIL import Image

    logger.debug("保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")
