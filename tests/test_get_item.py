import allure
import pytest

from api.models.avito.item_api import AvitoItemApi


@allure.feature("Получение объявления")
@allure.story("GET /api/1/item/{id}")
@pytest.mark.api
class TestGetItem(AvitoItemApi):
    """TC-004, TC-403."""

    @allure.title("TC-004: Получение объявления по существующему id")
    def test_get_by_existing_id(self, api_client, created_item):
        with allure.step("Получить id созданного объявления"):
            item_id = created_item["id"]
        with allure.step("Запросить объявление по id"):
            response = self.get_item(api_client, item_id)
        with allure.step("Проверка структуры ответа: id, name, price, sellerId, statistics, createdAt"):
            items = response if isinstance(response, list) else [response]
            assert len(items) >= 1
            found = next((i for i in items if i.get("id") == item_id), items[0])
            assert found["id"] == item_id
            assert "name" in found
            assert "price" in found
            assert "sellerId" in found
            assert "statistics" in found
            assert "createdAt" in found

    @allure.title("TC-403: Валидация структуры ответа")
    def test_response_structure(self, api_client, created_item):
        with allure.step("Получить id созданного объявления"):
            item_id = created_item["id"]
        with allure.step("Запросить объявление"):
            response = self.get_item(api_client, item_id)
        with allure.step("Проверка типов и наличия полей: id, sellerId, name, price, statistics, createdAt"):
            items = response if isinstance(response, list) else [response]
            item = items[0]
            assert "id" in item and isinstance(item["id"], str)
            assert "sellerId" in item
            assert "name" in item
            assert "price" in item
            assert "statistics" in item
            assert "likes" in item["statistics"] or "viewCount" in item["statistics"]
            assert "createdAt" in item
