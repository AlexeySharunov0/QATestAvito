import allure
import pytest

from api.models.avito.item_api import AvitoItemApi, generate_item_data


@allure.feature("E2E")
@pytest.mark.api
class TestE2ECreateGet(AvitoItemApi):
    """TC-301, TC-302, TC-303."""

    @allure.title("TC-301: Создание → получение по id")
    def test_create_then_get_by_id(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных и создание объявления"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                name="E2E Test Item",
                price=12345,
            )
            created = self.create_item(api_client, data)
            item_id = created["id"]
        with allure.step("Получение объявления по id"):
            got = self.get_item(api_client, item_id)
        with allure.step("Проверка: name, price, sellerId совпадают"):
            items = got if isinstance(got, list) else [got]
            found = next((i for i in items if i.get("id") == item_id), items[0])
            assert found["name"] == "E2E Test Item"
            assert found["price"] == 12345
            assert found["sellerId"] == unique_seller_id

    @allure.title("TC-302: Создание → получение по sellerId")
    def test_create_then_get_by_seller(self, api_client, unique_seller_id):
        with allure.step("Создание объявления"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                name="E2E Seller Test",
            )
            created = self.create_item(api_client, data)
            item_id = created["id"]
        with allure.step("Получение объявлений по sellerId"):
            seller_items = self.get_items_by_seller(api_client, unique_seller_id)
        with allure.step("Проверка: созданное объявление в списке"):
            ids = [i["id"] for i in seller_items if isinstance(i, dict)]
            assert item_id in ids

    @allure.title("TC-303: Создание → получение статистики")
    def test_create_then_get_statistic(self, api_client, unique_seller_id):
        with allure.step("Создание объявления с заданной статистикой"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                likes=7,
                view_count=77,
                contacts=3,
            )
            created = self.create_item(api_client, data)
            item_id = created["id"]
        with allure.step("Получение статистики по id"):
            stats = self.get_statistic(api_client, item_id)
        with allure.step("Проверка: likes, viewCount, contacts совпадают"):
            stats_list = stats if isinstance(stats, list) else [stats]
            stat = stats_list[0] if stats_list else {}
            if isinstance(stat, dict):
                assert stat.get("likes") == 7
                assert stat.get("viewCount") == 77
                assert stat.get("contacts") == 3
