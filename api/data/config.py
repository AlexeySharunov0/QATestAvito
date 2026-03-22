from pydantic import ConfigDict
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """BaseModel с запретом лишних полей (для запросов)."""

    model_config = ConfigDict(extra="forbid")


class BaseModelIgnoreExtra(PydanticBaseModel):
    """BaseModel, игнорирующий лишние поля (для ответов API)."""

    model_config = ConfigDict(extra="ignore")
