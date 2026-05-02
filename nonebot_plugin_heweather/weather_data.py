import asyncio

from httpx import URL, AsyncClient, Response
from nonebot.log import logger

from .config import plugin_config
from .model import AirApi, DailyApi, HourlyApi, NowApi, WarningApi
from .types import APIError, CityNotFoundError
from .utils import get_jwt_token


class Weather:
    def __url__(self):
        self.host = URL(plugin_config.qweather_apihost)

    def _forecast_days(self):
        self.forecast_days = plugin_config.qweather_forecase_days

    def __init__(self, city_name: str):
        self.city_name = city_name
        self.__url__()
        self._forecast_days()
        self.__reference = "\n请参考: https://dev.qweather.com/docs/start/status-code/"

    async def load_data(self):
        city_info = await self._get_city_info()
        self.city_id = city_info["id"]
        self.city_lat = city_info["lat"]
        self.city_lon = city_info["lon"]
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

    async def _get_data(self, url: URL, params: dict) -> Response:
        headers = {
            "Authorization": f"Bearer {get_jwt_token()}",
        }

        async with AsyncClient() as client:
            res = await client.get(url, params=params, headers=headers)
        return res

    async def _get_city_info(self):
        url = self.host.join("/geo/v2/city/lookup")
        res = await self._get_data(
            url=url,
            params={"location": self.city_name, "number": 1},
        )

        res = res.json()

        if res["code"] == "404":
            raise CityNotFoundError()
        elif res["code"] != "200":
            raise APIError("错误! 错误代码: {}".format(res["code"]) + self.__reference)
        else:
            location = res["location"][0]
            self.city_name = location["name"]
            return {
                "id": location["id"],
                "lat": location["lat"],
                "lon": location["lon"],
            }

    def _data_validate(self):
        if self.now.code == "200" and self.daily.code == "200":
            pass
        else:
            raise APIError(
                "错误! 请检查配置! "
                f"错误代码: now: {self.now.code}  "
                f"daily: {self.daily.code}  "
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
        url = self.host.join("/v7/weather/now")
        res = await self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return NowApi(**res.json())

    @property
    async def _daily(self) -> DailyApi:
        url = self.host.join(f"/v7/weather/{self.forecast_days}d")
        res = await self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return DailyApi(**res.json())

    @property
    async def _air(self) -> AirApi:
        lat = f"{float(self.city_lat):.2f}"
        lon = f"{float(self.city_lon):.2f}"
        url = self.host.join(f"/airquality/v1/current/{lat}/{lon}")
        res = await self._get_data(url=url, params={})
        self._check_response(res)
        return AirApi(**res.json())

    @property
    async def _warning(self) -> WarningApi | None:
        url = self.host.join("/v7/warning/now")
        res = await self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return None if res.json().get("code") == "204" else WarningApi(**res.json())

    @property
    async def _hourly(self) -> HourlyApi:
        url = self.host.join("/v7/weather/24h")
        res = await self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return HourlyApi(**res.json())
