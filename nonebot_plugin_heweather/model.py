from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Extra


class Now(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    obsTime: str
    temp: str
    icon: str
    text: str
    windScale: str
    windDir: str
    humidity: str
    precip: str
    vis: str


class NowApi(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    code: str
    now: Now


class Daily(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    fxDate: str
    week: Optional[str]
    date: Optional[str]
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str
    iconDay: str
    iconNight: str


class DailyApi(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    code: str
    daily: List[Daily]


class Air(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    category: str
    aqi: str
    pm2p5: str
    pm10: str
    o3: str
    co: str
    no2: str
    so2: str
    tag_color: Optional[str]


class AirApi(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    code: str
    now: Optional[Air]


class Warning(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    title: str
    type: str
    pubTime: str
    text: str


class WarningApi(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    code: str
    warning: Optional[List[Warning]]


class Hourly(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    fxTime: str
    hour: Optional[str]
    temp: str
    icon: str
    text: str
    temp_percent: Optional[str]


class HourlyApi(BaseModel):
    model_config = ConfigDict(extra=Extra.allow)
    code: str
    hourly: List[Hourly]


class HourlyType(IntEnum):
    current_12h = 1
    current_24h = 2
