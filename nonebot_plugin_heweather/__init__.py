from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")

from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Target,
    UniMessage,
    get_target,
    on_alconna,
)

from .config import Config, plugin_config
from .render_pic import render
from .schedule import (
    PushSubscription,
    load_subscriptions,
    register_push_job,
    remove_push_job,
    save_subscriptions,
)
from .weather_data import CityNotFoundError, Weather

__plugin_meta__ = PluginMetadata(
    name="和风天气",
    description="和风天气图片显示插件，支持每日定时推送",
    usage=(
        "天气地名 / 地名天气 - 查询天气\n"
        "天气订阅 城市 HH:MM - 订阅每日推送\n"
        "天气取消订阅 - 取消订阅\n"
        "天气订阅状态 - 查看订阅"
    ),
    type="application",
    homepage="https://github.com/kexue-z/nonebot-plugin-heweather",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)


if plugin_config.debug:
    logger.debug("将会保存图片到 weather.png")


def _target_key(target: Target) -> str:
    if target.private:
        return f"user:{target.id}"
    return f"group:{target.id}"


weather = on_alconna(
    Alconna("天气", Args["city", str]),
    block=True,
    priority=5,
    use_cmd_start=False,
)
weather.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
weather.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})


@weather.handle()
async def _(matcher: Matcher, city: str):
    w_data = Weather(city_name=city)
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


weather_sub = on_alconna(
    Alconna("天气订阅", Args["city", str], Args["time", str]),
    block=True,
    priority=1,
    use_cmd_start=False,
)


@weather_sub.handle()
async def _(
    matcher: Matcher, city: str, time: str, target: Target = Depends(get_target)
):
    try:
        hour, minute = map(int, time.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except ValueError:
        await matcher.finish("时间格式错误，请使用 HH:MM，例如 08:30")

    target_key = _target_key(target)

    try:
        w = Weather(city_name=city)
        await w.load_data()
        city = w.city_name
    except CityNotFoundError:
        await matcher.finish(f"找不到城市: {city}")

    sub = PushSubscription(city=city, hour=hour, minute=minute)
    subs = load_subscriptions()
    subs[target_key] = sub
    save_subscriptions(subs)
    register_push_job(target_key, sub)

    await matcher.finish(f"已订阅 {city} 每日 {hour:02d}:{minute:02d} 天气推送")


weather_unsub = on_alconna(
    Alconna("天气取消订阅"),
    block=True,
    priority=1,
    use_cmd_start=False,
)


@weather_unsub.handle()
async def _(matcher: Matcher, target: Target = Depends(get_target)):
    target_key = _target_key(target)

    subs = load_subscriptions()
    if target_key not in subs:
        await matcher.finish("当前没有订阅")

    city = subs[target_key].city
    del subs[target_key]
    save_subscriptions(subs)
    remove_push_job(target_key)

    await matcher.finish(f"已取消 {city} 的天气推送订阅")


weather_sub_status = on_alconna(
    Alconna("天气订阅状态"),
    block=True,
    priority=1,
    use_cmd_start=False,
)


@weather_sub_status.handle()
async def _(matcher: Matcher, target: Target = Depends(get_target)):
    target_key = _target_key(target)
    subs = load_subscriptions()

    if target_key not in subs:
        await matcher.finish("当前没有订阅")

    sub = subs[target_key]
    status = "启用" if sub.enabled else "停用"
    await matcher.finish(
        f"城市: {sub.city}\n时间: {sub.hour:02d}:{sub.minute:02d}\n状态: {status}"
    )
