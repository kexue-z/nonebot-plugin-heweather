from nonebot.plugin import require
from pathlib import Path

template_to_html = require("nonebot_plugin_htmlrender").template_to_html
html_to_pic = require("nonebot_plugin_htmlrender").html_to_pic


async def render(data) -> bytes:
    data = add_week(data)
    html = await template_to_html(
        template_path=str(Path(__file__).parent / "templates"),
        template_name="weather.html",
        now=convert_now(data),
        days=convert_days(data),
        city=convert_city(data),
        warning=convert_warning(data),
    )
    with open("test.html","w+") as f:
        f.write(html)
    return await html_to_pic(html, viewport={"width": 1000, "height": 300})


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
