import allure
import pytest

from api.models.avito.item_api import AvitoItemApi, generate_item_data


@allure.feature("Объявления продавца")
@allure.story("GET /api/1/{sellerId}/item")
@pytest.mark.api
class TestGetBySeller(AvitoItemApi):
    """TC-005, TC-006, TC-304."""

    @allure.title("TC-005: Получение объявлений продавца с объявлениями")
    def test_get_items_by_seller_with_items(self, api_client, created_item):
        with allure.step("Получить sellerId и item_id из созданного объявления"):
            seller_id = created_item["sellerId"]
            item_id = created_item["id"]
        with allure.step("Запросить объявления по sellerId"):
            response = self.get_items_by_seller(api_client, seller_id)
        with allure.step("Проверка: список содержит созданное объявление, все с нужным sellerId"):
            assert isinstance(response, list)
            ids = [i["id"] for i in response if isinstance(i, dict)]
            assert item_id in ids
            for item in response:
                if isinstance(item, dict):
                    assert item["sellerId"] == seller_id

    @allure.title("TC-006: Получение объявлений продавца без объявлений")
    def test_get_items_by_seller_empty(self, api_client, unique_seller_id):
        with allure.step("Запросить объявления по sellerId без объявлений"):
            response = self.get_items_by_seller(api_client, unique_seller_id)
        with allure.step("Проверка: пустой список или все с нужным sellerId"):
            assert isinstance(response, list)
            assert response == [] or all(i.get("sellerId") == unique_seller_id for i in response)

    @allure.title("TC-304: Несколько объявлений одного продавца")
    def test_multiple_items_same_seller(self, api_client, unique_seller_id):
        with allure.step("Создать 3 объявления одного продавца"):
            for _ in range(3):
                self.create_item(api_client, generate_item_data(seller_id=unique_seller_id))
        with allure.step("Запросить объявления по sellerId"):
            response = self.get_items_by_seller(api_client, unique_seller_id)
        with allure.step("Проверка: минимум 3 объявления, все с нужным sellerId"):
            assert len(response) >= 3
            for item in response:
                assert item["sellerId"] == unique_seller_id
