from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    qweather_apikey: str
    qweather_apitype: str
    DEBUG: bool