from datetime import datetime
from typing import Any, Callable

import orjson
from pydantic import BaseModel, model_validator
from zoneinfo import ZoneInfo


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}
        allow_population_by_field_name = True

    @model_validator(mode="before")
    def set_null_microseconds(cls, values: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in values.items()
            if isinstance(v, datetime)
        }

        return {**values, **datetime_fields}
