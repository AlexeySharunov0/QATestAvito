from __future__ import annotations

from typing import Optional

from pydantic import Field

from api.data.config import BaseModel, BaseModelIgnoreExtra


############################################ Запрос создания объявления

class ItemStatisticsRequest(BaseModel):
    """Статистика при создании. API требует likes, viewCount, contacts >= 1."""

    likes: int = Field(..., ge=1, description="см. BUGS.md")
    viewCount: int = Field(..., ge=1)
    contacts: int = Field(..., ge=1)


class ItemCreateRequest(BaseModel):
    """Тело запроса POST /api/1/item — создание объявления."""

    sellerID: int
    name: str = Field(..., min_length=1)
    price: int = Field(..., ge=0)
    statistics: ItemStatisticsRequest


############################################ Ответы API

class ItemStatistics(BaseModelIgnoreExtra):
    """Статистика в ответе (может быть 0)."""

    likes: int = Field(..., ge=0)
    viewCount: int = Field(..., ge=0)
    contacts: int = Field(..., ge=0)


class ItemResponse(BaseModelIgnoreExtra):
    """Объявление в ответе GET /api/1/item/{id} и GET /api/1/{sellerId}/item.
    POST create может вернуть status вместо полного JSON — тогда createdAt отсутствует.
    """

    id: str = Field(..., min_length=1)
    sellerId: int
    name: str
    price: int
    statistics: ItemStatistics
    createdAt: Optional[str] = None


class StatisticResponse(BaseModelIgnoreExtra):
    """Статистика по объявлению GET /api/1/statistic/{id}."""

    likes: int = Field(..., ge=0)
    viewCount: int = Field(..., ge=0)
    contacts: int = Field(..., ge=0)
