import asyncio
from typing import Optional

from httpx import AsyncClient, Response
from nonebot.log import logger

from .config import QWEATHER_FORECASE_DAYS
from .model import AirApi, DailyApi, HourlyApi, NowApi, WarningApi


class APIError(Exception): ...


class ConfigError(Exception): ...


class CityNotFoundError(Exception): ...


class Weather:
    def __url__(self):
        self.url_geoapi = "https://geoapi.qweather.com/v2/city/"
        if self.api_type == 2 or self.api_type == 1:
            self.url_weather_api = "https://api.qweather.com/v7/weather/"
            self.url_weather_warning = "https://api.qweather.com/v7/warning/now"
            self.url_air = "https://api.qweather.com/v7/air/now"
            self.url_hourly = "https://api.qweather.com/v7/weather/24h"

            logger.info("使用标准订阅API")

        elif self.api_type == 0:
            self.url_weather_api = "https://devapi.qweather.com/v7/weather/"
            self.url_weather_warning = "https://devapi.qweather.com/v7/warning/now"
            self.url_air = "https://devapi.qweather.com/v7/air/now"
            self.url_hourly = "https://devapi.qweather.com/v7/weather/24h"

            logger.info("使用免费订阅API")
        else:
            raise ConfigError(
                "api_type 必须是为 (int)0 -> 免费订阅, "
                "(int)1 -> 标准订阅, (int)2 -> 商业版"
                f"\n当前为: ({type(self.api_type)}){self.api_type}"
            )

    def _forecast_days(self):
        self.forecast_days = QWEATHER_FORECASE_DAYS
        if self.forecast_days:
            if self.api_type == 0 and not (3 <= self.forecast_days <= 7):
                raise ConfigError("api_type = 0 免费订阅 预报天数必须 3<= x <=7")

    def __init__(self, city_name: str, api_key: str, api_type: int = 0):
        self.city_name = city_name
        self.apikey = api_key
        self.api_type = api_type
        self.__url__()

        self._forecast_days()

        # self.now: Optional[Dict[str, str]] = None
        # self.daily = None
        # self.air = None
        # self.warning = None
        self.__reference = "\n请参考: https://dev.qweather.com/docs/start/status-code/"

    async def load_data(self):
        self.city_id = await self._get_city_id()
        (
            self.now,
            self.daily,
            self.air,
            self.warning,
            self.hourly,
        ) = await asyncio.gather(
            self._now, self._daily, self._air, self._warning, self._hourly
        )
        self._data_validate()

    async def _get_data(self, url: str, params: dict) -> Response:
        async with AsyncClient() as client:
            res = await client.get(url, params=params)
        return res

    async def _get_city_id(self, api_type: str = "lookup"):
        res = await self._get_data(
            url=self.url_geoapi + api_type,
            params={"location": self.city_name, "key": self.apikey, "number": 1},
        )

        res = res.json()
        logger.debug(res)
        if res["code"] == "404":
            raise CityNotFoundError()
        elif res["code"] != "200":
            raise APIError("错误! 错误代码: {}".format(res["code"]) + self.__reference)
        else:
            self.city_name = res["location"][0]["name"]
            return res["location"][0]["id"]

    def _data_validate(self):
        if self.now.code == "200" and self.daily.code == "200":
            pass
        else:
            raise APIError(
                "错误! 请检查配置! "
                f"错误代码: now: {self.now.code}  "
                f"daily: {self.daily.code}  "
                + "air: {}  ".format(self.air.code if self.air else "None")
                + "warning: {}".format(self.warning.code if self.warning else "None")
                + self.__reference
            )

    def _check_response(self, response: Response) -> bool:
        if response.status_code == 200:
            logger.debug(f"{response.json()}")
            return True
        else:
            raise APIError(f"Response code:{response.status_code}")

    @property
    async def _now(self) -> NowApi:
        res = await self._get_data(
            url=self.url_weather_api + "now",
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_response(res)
        return NowApi(**res.json())

    @property
    async def _daily(self) -> DailyApi:
        res = await self._get_data(
            url=self.url_weather_api + str(self.forecast_days) + "d",
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_response(res)
        return DailyApi(**res.json())

    @property
    async def _air(self) -> AirApi:
        res = await self._get_data(
            url=self.url_air,
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_response(res)
        return AirApi(**res.json())

    @property
    async def _warning(self) -> Optional[WarningApi]:
        res = await self._get_data(
            url=self.url_weather_warning,
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_response(res)
        return None if res.json().get("code") == "204" else WarningApi(**res.json())

    @property
    async def _hourly(self) -> HourlyApi:
        res = await self._get_data(
            url=self.url_hourly,
            params={"location": self.city_id, "key": self.apikey},
        )
        self._check_response(res)
        return HourlyApi(**res.json())
