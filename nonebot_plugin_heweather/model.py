from enum import IntEnum

from nonebot.compat import PYDANTIC_V2, ConfigDict
from pydantic import BaseModel


class Now(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

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
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    now: Now


class Daily(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    fxDate: str
    week: str | None = None
    date: str | None = None
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str
    iconDay: str
    iconNight: str


class DailyApi(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    daily: list[Daily]


class Air(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    category: str
    aqi: str
    pm2p5: str
    pm10: str
    o3: str
    co: str
    no2: str
    so2: str
    tag_color: str | None = None


class AirApi(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    now: Air | None = None


class Warning(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    title: str
    type: str
    pubTime: str
    text: str


class WarningApi(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    warning: list[Warning] | None = None


class Hourly(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    fxTime: str
    hour: str | None = None
    temp: str
    icon: str
    text: str
    temp_percent: str | None = None


class HourlyApi(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    hourly: list[Hourly]


class HourlyType(IntEnum):
    current_12h = 1
    current_24h = 2
