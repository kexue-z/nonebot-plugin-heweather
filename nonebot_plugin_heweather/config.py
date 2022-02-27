from pydantic import BaseModel, Extra
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    qweather_apikey: Optional[str] = None
    qweather_apitype: Optional[str] = None
    debug: bool = False
