from nonebot.log import logger
from httpx import AsyncClient
import nonebot

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
    logger.info("使用商业版API")
else:
    url_weather_api = "https://devapi.qweather.com/v7/weather/"
    url_geoapi = "https://geoapi.qweather.com/v2/city/"
    url_weather_warning = "https://devapi.qweather.com/v7/warning/now"
    logger.info("使用开发版API")

# 获取城市ID
async def get_Location(city_kw: str, api_type: str = "lookup") -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_geoapi + api_type, params={"location": city_kw, "key": apikey}
        )
        return res.json()


# 获取天气信息
async def get_WeatherInfo(api_type: str, city_id: str) -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_weather_api + api_type, params={"location": city_id, "key": apikey}
        )
        return res.json()


# 获取天气灾害预警
async def get_WeatherWarning(city_id: str) -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_weather_warning,
            params={"location": city_id, "key": apikey},
        )
        res = res.json()
    return res if res["code"] == "200" and res["warning"] else None


# 获取天气信息
async def get_City_Weather(city: str):
    city_info = await get_Location(city)
    logger.debug(city_info)
    city_id = city_info["location"][0]["id"]

    daily_info = await get_WeatherInfo("7d", city_id)
    logger.debug(daily_info)
    
    now_info = await get_WeatherInfo("now", city_id)
    logger.debug(now_info)
    
    warning = await get_WeatherWarning(city_id)
    logger.debug(warning)
    
    if (
        city_info["code"] == "200"
        and daily_info["code"] == "200"
        and now_info["code"] == "200"
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
        }
    else:
        logger.error(
            f'错误: {city_info["code"]},{daily_info["code"]},{now_info["code"]},{warning} 请参考 https://dev.qweather.com/docs/start/status-code/ '
        )
        return int(daily_info["code"])
