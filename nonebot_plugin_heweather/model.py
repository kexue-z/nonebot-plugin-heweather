from enum import IntEnum
from typing import List, Optional

from pydantic import Extra, BaseModel


class Now(BaseModel, extra=Extra.allow):
    obsTime: str
    temp: str
    icon: str
    text: str
    windScale: str
    windDir: str
    humidity: str
    precip: str
    vis: str


class NowApi(BaseModel, extra=Extra.allow):
    code: str
    now: Now


class Daily(BaseModel, extra=Extra.allow):
    fxDate: str
    week: Optional[str]
    date: Optional[str]
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str
    iconDay: str
    iconNight: str


class DailyApi(BaseModel, extra=Extra.allow):
    code: str
    daily: List[Daily]


class Air(BaseModel, extra=Extra.allow):
    category: str
    aqi: str
    pm2p5: str
    pm10: str
    o3: str
    co: str
    no2: str
    so2: str
    tag_color: Optional[str]


class AirApi(BaseModel, extra=Extra.allow):
    code: str
    now: Optional[Air]


class Warning(BaseModel, extra=Extra.allow):
    title: str
    type: str
    pubTime: str
    text: str


class WarningApi(BaseModel, extra=Extra.allow):
    code: str
    warning: Optional[List[Warning]]


class Hourly(BaseModel, extra=Extra.allow):
    fxTime: str
    hour: Optional[str]
    temp: str
    icon: str
    text: str
    temp_percent: Optional[str]


class HourlyApi(BaseModel, extra=Extra.allow):
    code: str
    hourly: List[Hourly]


class HourlyType(IntEnum):
    current_12h = 1
    current_24h = 2
