from __future__ import annotations

import random
import re
import string
from typing import Any

import allure

from api.data.item import ItemCreateRequest, ItemResponse, StatisticResponse
from api.utils.client import AvitoApiClient


class AvitoApiUrls:
    """Константы эндпоинтов API объявлений."""

    CREATE_ITEM = "item"
    GET_ITEM = "item/{id}"
    GET_ITEMS_BY_SELLER = "{seller_id}/item"
    GET_STATISTIC = "statistic/{id}"


def generate_seller_id() -> int:
    """Генерирует уникальный sellerId в диапазоне 111111–999999."""
    return random.randint(111111, 999999)


def generate_item_data(
    seller_id: int | None = None,
    name: str | None = None,
    price: int = 1000,
    likes: int = 1,
    view_count: int = 1,
    contacts: int = 1,
    **overrides: Any,
) -> dict[str, Any]:
    """
    Формирует валидный payload для создания объявления.
    API требует likes, viewCount, contacts в statistics (см. BUGS.md).
    """
    data = {
        "sellerID": seller_id or generate_seller_id(),
        "name": name or f"Test Item {''.join(random.choices(string.ascii_lowercase, k=8))}",
        "price": price,
        "statistics": {
            "likes": likes,
            "viewCount": view_count,
            "contacts": contacts,
        },
    }
    if overrides:
        if "statistics" in overrides:
            data["statistics"].update(overrides.pop("statistics"))
        data.update(overrides)
    return data


class AvitoItemApi(AvitoApiUrls):
    """Обёртки над методами API объявлений."""

    @allure.step("Данные для объявления")
    def get_item_data(self, item_params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Возвращает данные для создания объявления с возможностью переопределения."""
        params = generate_item_data()
        if item_params:
            params.update(item_params)
        return params

    @allure.step("Создание объявления")
    def create_item(
        self,
        client: AvitoApiClient,
        data: dict[str, Any],
        expected_status: int | list[int] = 200,
    ) -> dict:
        """
        Создаёт объявление.
        Возвращает dict с id (извлекается из status, если API не вернул id в теле).
        """
        response = client.post(
            self.CREATE_ITEM,
            json=data,
            expected_status_code=expected_status,
        )
        if isinstance(response, dict) and "id" not in response and "status" in response:
            match = re.search(
                r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                str(response.get("status", "")),
                re.I,
            )
            if match:
                response = {
                    "id": match.group(0),
                    "sellerId": data.get("sellerID"),
                    "name": data.get("name"),
                    "price": data.get("price"),
                    "statistics": data.get("statistics", {}),
                }
        if isinstance(response, dict) and "id" in response:
            ItemResponse.model_validate(response)
        return response

    @allure.step("Создание объявления с ожидаемой ошибкой")
    def create_item_400(
        self,
        client: AvitoApiClient,
        data: dict[str, Any],
    ) -> None:
        """Создание с ожидаемым статусом 400."""
        client.post(self.CREATE_ITEM, json=data, expected_status_code=400)

    @allure.step("Получение объявления по id")
    def get_item(
        self,
        client: AvitoApiClient,
        item_id: str,
        expected_status: int | list[int] = 200,
    ) -> dict | list:
        """Получает объявление по идентификатору."""
        result = client.get(
            self.GET_ITEM.format(id=item_id),
            expected_status_code=expected_status,
        )
        if expected_status == 200 or (isinstance(expected_status, list) and 200 in expected_status):
            for obj in (result if isinstance(result, list) else [result]):
                if isinstance(obj, dict) and "id" in obj:
                    ItemResponse.model_validate(obj)
        return result

    @allure.step("Получение объявлений по sellerId")
    def get_items_by_seller(
        self,
        client: AvitoApiClient,
        seller_id: int,
        expected_status: int | list[int] = 200,
    ) -> list:
        """Возвращает все объявления продавца."""
        result = client.get(
            self.GET_ITEMS_BY_SELLER.format(seller_id=seller_id),
            expected_status_code=expected_status,
        )
        items = result if isinstance(result, list) else [result]
        for obj in items:
            if isinstance(obj, dict) and "id" in obj:
                ItemResponse.model_validate(obj)
        return items

    @allure.step("Получение статистики по объявлению")
    def get_statistic(
        self,
        client: AvitoApiClient,
        item_id: str,
        expected_status: int | list[int] = 200,
    ) -> dict | list:
        """Получает статистику по идентификатору объявления."""
        result = client.get(
            self.GET_STATISTIC.format(id=item_id),
            expected_status_code=expected_status,
        )
        if expected_status == 200 or (isinstance(expected_status, list) and 200 in expected_status):
            for obj in (result if isinstance(result, list) else [result]):
                if isinstance(obj, dict) and "likes" in obj:
                    StatisticResponse.model_validate(obj)
        return result
