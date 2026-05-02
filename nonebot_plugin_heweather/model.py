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


class AirColor(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    red: int
    green: int
    blue: int
    alpha: float


class AirPrimaryPollutant(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    name: str | None = None
    fullName: str | None = None


class AirHealthAdvice(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    generalPopulation: str | None = None
    sensitivePopulation: str | None = None


class AirHealth(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    effect: str | None = None
    advice: AirHealthAdvice | None = None


class AirQualityIndex(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    name: str
    aqi: float
    aqiDisplay: str
    level: str | None = None
    category: str | None = None
    color: AirColor | None = None
    primaryPollutant: AirPrimaryPollutant | None = None
    health: AirHealth | None = None


class AirConcentration(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    value: float
    unit: str


class AirSubIndex(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    aqi: float | None = None
    aqiDisplay: str | None = None


class AirPollutant(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    code: str
    name: str
    fullName: str | None = None
    concentration: AirConcentration
    subIndexes: list[AirSubIndex] | None = None


class AirStation(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    id: str
    name: str


class Air(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    category: str | None = None
    aqi: str
    aqiDisplay: str | None = None
    level: str | None = None
    color: AirColor | None = None
    primaryPollutant: str | None = None
    effect: str | None = None
    pm2p5: str | None = None
    pm10: str | None = None
    o3: str | None = None
    co: str | None = None
    no2: str | None = None
    so2: str | None = None


class AirApi(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"

    indexes: list[AirQualityIndex]
    pollutants: list[AirPollutant]
    stations: list[AirStation] | None = None


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
