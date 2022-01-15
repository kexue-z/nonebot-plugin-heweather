from typing import Union

import nonebot
from httpx import AsyncClient
from nonebot.log import logger

apikey = nonebot.get_driver().config.qweather_apikey
if not apikey:
    raise ValueError(f"请在环境变量中添加 qweather_apikey 参数")

commercial: bool = (
    False if not nonebot.get_driver().config.qweather_commercial else True
)
if commercial:
    url_weather_api = "https://api.qweather.com/v7/weather/"
    url_geoapi = "https://geoapi.qweather.com/v2/city/"
    url_weather_warning = "https://api.qweather.com/v7/warning/now"
    url_air = "https://api.qweather.com/v7/air/now"
    logger.info("使用商业版API")
else:
    url_weather_api = "https://devapi.qweather.com/v7/weather/"
    url_geoapi = "https://geoapi.qweather.com/v2/city/"
    url_weather_warning = "https://devapi.qweather.com/v7/warning/now"
    url_air = "https://devapi.qweather.com/v7/air/now"
    logger.info("使用开发版API")


async def get_location(city_kw: str, api_type: str = "lookup") -> dict:
    """获取城市ID

    Args:
        city_kw (str): 关键词
        api_type (str, optional): 查询方式. Defaults to "lookup".

    Returns:
        dict: 查询结果列表
    """
    async with AsyncClient() as client:
        res = await client.get(
            url_geoapi + api_type, params={"location": city_kw, "key": apikey}
        )
        return res.json()


async def get_weatherinfo(api_type: str, city_id: str) -> dict:
    """获取天气信息

    Args:
        api_type (str): 类型
        city_id (str): 城市id

    Returns:
        dict: 天气信息
    """
    async with AsyncClient() as client:
        res = await client.get(
            url_weather_api + api_type, params={"location": city_id, "key": apikey}
        )
        return res.json()


async def get_weatherwarning(city_id: str) -> dict:
    """获取天气灾害预警

    Args:
        city_id (str): 城市id

    Returns:
        dict: 灾害预警信息
    """
    async with AsyncClient() as client:
        res = await client.get(
            url_weather_warning,
            params={"location": city_id, "key": apikey},
        )
        res = res.json()
    return res if res["code"] == "200" and res["warning"] else None


async def get_air(city_id: str) -> dict:
    async with AsyncClient() as client:
        res = await client.get(url_air, params={"location": city_id, "key": apikey})
        res = res.json()
    return res


async def get_city_weather(city: str) -> Union[dict, int]:
    """获取天气信息

    Args:
        city (str): 城市名

    Returns:
        Union[dict, int]: 返回dict 或 错误代码
    """

    city_info = await get_location(city)
    logger.debug(city_info)
    city_id = city_info["location"][0]["id"]

    daily_info = await get_weatherinfo("7d", city_id)
    logger.debug(daily_info)

    now_info = await get_weatherinfo("now", city_id)
    logger.debug(now_info)

    air_info = await get_air(city_id)
    logger.debug(air_info)

    warning = await get_weatherwarning(city_id)
    logger.debug(warning)

    if (
        city_info["code"] == "200"
        and daily_info["code"] == "200"
        and now_info["code"] == "200"
        and air_info["code"] == "200"
    ):
        city_name = city_info["location"][0]["name"]

        # 3天天气

        daily = daily_info["daily"]
        day1 = daily[0]
        day2 = daily[1]
        day3 = daily[2]
        day4 = daily[3]
        day5 = daily[4]
        day6 = daily[5]
        day7 = daily[6]

        # 实时天气

        now = now_info["now"]

        return {
            "city": city_name,
            "now": now,
            "day1": day1,
            "day2": day2,
            "day3": day3,
            "day4": day4,
            "day5": day5,
            "day6": day6,
            "day7": day7,
            "warning": warning,
            "air": air_info,
        }
    else:
        try:
            logger.error(
                f"""错误: 
                {city_info["code"]},
                {daily_info["code"]},
                {now_info["code"]},
                {air_info["code"]},
                {warning["code"]} 
                请参考 https://dev.qweather.com/docs/start/status-code/ """
            )
            return int(daily_info["code"])
        except:
            logger.error(
                f"""错误: 
                {city_info["code"]},
                {daily_info["code"]},
                {now_info["code"]},
                {air_info["code"]},
                {warning} 
                请参考 https://dev.qweather.com/docs/start/status-code/ """
            )
            return int(daily_info["code"])
