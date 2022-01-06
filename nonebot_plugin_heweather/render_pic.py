from pathlib import Path

from nonebot.plugin import require

template_to_pic = require("nonebot_plugin_htmlrender").template_to_pic

async def render(data) -> bytes:
    template_path = str(Path(__file__).parent / "templates")
    data = add_week(data)
    return await template_to_pic(
        template_path=template_path,
        template_name="weather.html",
        templates={
            "now": convert_now(data),
            "days": convert_days(data),
            "city": convert_city(data),
            "warning": convert_warning(data),
        },
        pages={
            "viewport": {"width": 1000, "height": 300},
            "base_url": f"file://{template_path}",
        },
    )

def convert_days(data):
    days = []
    for day in range(1, 8):
        days.append(data[f"day{str(day)}"])

    return days


def add_week(data):
    from datetime import datetime

    week_map = [
        "周日",
        "周一",
        "周二",
        "周三",
        "周四",
        "周五",
        "周六",
    ]
    for day in range(1, 8):
        date = data[f"day{str(day)}"]["fxDate"].split("-")
        _year = int(date[0])
        _month = int(date[1])
        _day = int(date[2])
        week = int(datetime(_year, _month, _day, 0, 0).strftime("%w"))
        data[f"day{str(day)}"]["week"] = week_map[week] if day != 1 else "今日"
        data[f"day{str(day)}"]["date"] = f"{_month}月{_day}日"
    return data


def convert_now(data):
    return data["now"]


def convert_warning(data):
    return data["warning"]


def convert_city(data):
    return data["city"]
