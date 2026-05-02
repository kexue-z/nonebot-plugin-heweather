from datetime import datetime
from pathlib import Path
import platform

from nonebot_plugin_htmlrender import template_to_pic

from .config import plugin_config
from .model import Air, AirApi, Daily, Hourly, HourlyType
from .weather_data import Weather


async def render(weather: Weather) -> bytes:
    template_path = str(Path(__file__).parent / "templates")

    air = None
    if weather.air:
        air = extract_air_data(weather.air)

    return await template_to_pic(
        template_path=template_path,
        template_name="weather.html",
        templates={
            "now": weather.now.now,
            "days": add_date(weather.daily.daily),
            "city": weather.city_name,
            "warning": weather.warning,
            "air": air,
            "hours": add_hour_data(weather.hourly.hourly),
        },
        pages={
            "viewport": {"width": 1000, "height": 300},
            "base_url": f"file://{template_path}",
        },
    )


def extract_air_data(air_api: AirApi) -> Air | None:
    index = _select_aqi_index(air_api.indexes)
    if not index:
        return None

    pollutants = {p.code: p for p in air_api.pollutants}

    primary_pollutant = None
    if index.primaryPollutant:
        primary_pollutant = index.primaryPollutant.name

    effect = None
    if index.health:
        effect = index.health.effect

    return Air(
        category=index.category,
        aqi=index.aqiDisplay,
        aqiDisplay=index.aqiDisplay,
        level=index.level,
        color=index.color,
        primaryPollutant=primary_pollutant,
        effect=effect,
        pm2p5=_get_pollutant_value(pollutants, "pm2p5"),
        pm10=_get_pollutant_value(pollutants, "pm10"),
        o3=_get_pollutant_value(pollutants, "o3"),
        co=_get_pollutant_value(pollutants, "co"),
        no2=_get_pollutant_value(pollutants, "no2"),
        so2=_get_pollutant_value(pollutants, "so2"),
    )


def _select_aqi_index(indexes):
    for idx in indexes:
        if idx.code == "qaqi":
            return idx
    for idx in indexes:
        if idx.code == "us-epa":
            return idx
    return indexes[0] if indexes else None


def _get_pollutant_value(pollutants: dict, code: str) -> str | None:
    pollutant = pollutants.get(code)
    if pollutant and pollutant.concentration:
        return str(pollutant.concentration.value)
    return None


def add_hour_data(hourly: list[Hourly]):
    min_temp = min([int(hour.temp) for hour in hourly])
    high = max([int(hour.temp) for hour in hourly])
    low = int(min_temp - (high - min_temp))
    for hour in hourly:
        date_time = datetime.fromisoformat(hour.fxTime)
        if platform.system() == "Windows":
            hour.hour = date_time.strftime("%#I%p")
        else:
            hour.hour = date_time.strftime("%-I%p")
        if high == low:
            hour.temp_percent = "100px"
        else:
            hour.temp_percent = f"{int((int(hour.temp) - low) / (high - low) * 100)}px"
    if plugin_config.qweather_hourlytype == HourlyType.current_12h:
        hourly = hourly[:12]
    if plugin_config.qweather_hourlytype == HourlyType.current_24h:
        hourly = hourly[::2]
    return hourly


def add_date(daily: list[Daily]):
    week_map = [
        "周日",
        "周一",
        "周二",
        "周三",
        "周四",
        "周五",
        "周六",
    ]

    for day in daily:
        date = day.fxDate.split("-")
        _year = int(date[0])
        _month = int(date[1])
        _day = int(date[2])
        week = int(datetime(_year, _month, _day, 0, 0).strftime("%w"))
        day.week = week_map[week] if day != 0 else "今日"
        day.date = f"{_month}月{_day}日"

    return daily
