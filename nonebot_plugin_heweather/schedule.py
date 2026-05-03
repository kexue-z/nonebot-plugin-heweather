import json
import traceback

from nonebot import get_driver, logger
from nonebot.compat import PYDANTIC_V2, ConfigDict
from nonebot.plugin import require
from nonebot_plugin_alconna import Image, Target, UniMessage
from pydantic import BaseModel, Field

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_localstore")

from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_localstore import get_plugin_data_file

from .render_pic import render
from .weather_data import CityNotFoundError, Weather

SUBSCRIPTIONS_FILE = get_plugin_data_file("subscriptions.json")


class PushSubscription(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    city: str
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)
    enabled: bool = True


def load_subscriptions() -> dict[str, PushSubscription]:
    if SUBSCRIPTIONS_FILE.exists():
        try:
            data = json.loads(SUBSCRIPTIONS_FILE.read_text(encoding="UTF-8"))
            return {k: PushSubscription(**v) for k, v in data.items()}
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to load subscriptions: {e}")
    return {}


def save_subscriptions(subs: dict[str, PushSubscription]) -> None:
    data = {k: v.model_dump() for k, v in subs.items()}
    SUBSCRIPTIONS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="UTF-8",
    )


def make_job_id(target_key: str) -> str:
    return f"heweather_push_{target_key}"


def register_push_job(target_key: str, sub: PushSubscription) -> None:
    job_id = make_job_id(target_key)

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    if sub.enabled:
        scheduler.add_job(
            push_weather,
            "cron",
            hour=sub.hour,
            minute=sub.minute,
            id=job_id,
            replace_existing=True,
            misfire_grace_time=300,
            kwargs={"target_key": target_key, "city": sub.city},
        )
        logger.info(
            f"Registered push job for {target_key}: "
            f"{sub.city} at {sub.hour:02d}:{sub.minute:02d}"
        )


def remove_push_job(target_key: str) -> None:
    job_id = make_job_id(target_key)
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"Removed push job for {target_key}")


async def push_weather(target_key: str, city: str) -> None:
    logger.info(f"Starting weather push for {target_key}, city: {city}")

    try:
        logger.debug(f"Fetching weather data for city: {city}")
        w_data = Weather(city_name=city)
        await w_data.load_data()
        logger.debug(f"Weather data loaded successfully for {city}")

        logger.debug(f"Rendering weather image for {city}")
        img = await render(w_data)
        logger.debug(f"Weather image rendered, size: {len(img)} bytes")
    except CityNotFoundError:
        logger.error(f"Push failed: city '{city}' not found")
        return
    except Exception as e:
        logger.error(f"Push failed for {target_key}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return

    try:
        target_type, target_id = target_key.split(":", 1)
        logger.debug(f"Sending to {target_type}: {target_id}")

        if target_type == "group":
            target = Target.group(target_id)
        elif target_type == "user":
            target = Target.user(target_id)
        else:
            logger.error(f"Unknown target type: {target_type}")
            return

        await UniMessage(Image(raw=img)).send(target=target)
        logger.info(f"Weather push sent to {target_key} for {city}")
    except Exception as e:
        logger.error(f"Failed to send push to {target_key}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")


@get_driver().on_startup
async def load_push_jobs() -> None:
    subs = load_subscriptions()
    for target_key, sub in subs.items():
        register_push_job(target_key, sub)
    logger.info(f"Loaded {len(subs)} weather push subscriptions")
