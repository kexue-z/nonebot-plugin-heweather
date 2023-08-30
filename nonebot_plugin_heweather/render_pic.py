import platform
from datetime import datetime
from typing import List
from pathlib import Path

from nonebot import require

require("nonebot_plugin_htmlrender")

from nonebot_plugin_htmlrender import template_to_pic

from .config import QWEATHER_HOURLYSTYLE, QWEATHER_HOURLYTYPE
from .model import Air, Daily, Hourly, HourlyStyle, HourlyType
from .weather_data import Weather


async def render(weather: Weather) -> bytes:
    template_path = str(Path(__file__).parent / "templates")

    air = None
    if weather.air:
        if weather.air.now:
            air = add_tag_color(weather.air.now)

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
            "hourly_style": QWEATHER_HOURLYSTYLE,
            "curr_hour": int(
                datetime.fromisoformat(weather.now.now.obsTime).strftime("%I")
            ),
        },
        pages={
            "viewport": {"width": 1000, "height": 300},
            "base_url": f"file://{template_path}",
        },
    )


def add_hour_data(hourly: List[Hourly]):
    min_temp = min([int(hour.temp) for hour in hourly])
    high = max([int(hour.temp) for hour in hourly])
    low = int(min_temp - (high - min_temp))
    for hour in hourly:
        date_time = datetime.fromisoformat(hour.fxTime)
        if platform.system() == "Windows":
            hour.hour = date_time.strftime("%#I%p")
        else:
            hour.hour = date_time.strftime("%-I%p")
        hour.temp_percent = f"{int((int(hour.temp) - low) / (high - low) * 100)}px"
        hour.hour_key = int(date_time.strftime("%I"))
    if QWEATHER_HOURLYSTYLE == HourlyStyle.clock:
        hourly.sort(key=lambda x: x.hour_key)
    else:
        if QWEATHER_HOURLYTYPE == HourlyType.current_12h:
            hourly = hourly[:12]
        if QWEATHER_HOURLYTYPE == HourlyType.current_24h:
            hourly = hourly[::2]
    return hourly


def add_date(daily: List[Daily]):
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


def add_tag_color(air: Air):
    color = {
        "优": "#95B359",
        "良": "#A9A538",
        "轻度污染": "#E0991D",
        "中度污染": "#D96161",
        "重度污染": "#A257D0",
        "严重污染": "#D94371",
    }
    air.tag_color = color[air.category]
    return air
