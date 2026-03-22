import allure
import pytest

from api.models.avito.item_api import AvitoItemApi


@allure.feature("Статистика")
@allure.story("GET /api/1/statistic/{id}")
@pytest.mark.api
class TestGetStatistic(AvitoItemApi):
    """TC-007."""

    @allure.title("TC-007: Получение статистики по существующему объявлению")
    def test_get_statistic_existing_item(self, api_client, created_item):
        with allure.step("Получить id созданного объявления"):
            item_id = created_item["id"]
        with allure.step("Запросить статистику по id"):
            response = self.get_statistic(api_client, item_id)
        with allure.step("Проверка наличия полей likes/viewCount/contacts"):
            stats_list = response if isinstance(response, list) else [response]
            assert len(stats_list) >= 1
            stats = stats_list[0] if isinstance(stats_list[0], dict) else stats_list
            assert isinstance(stats, dict)
            assert "likes" in stats or "viewCount" in stats or "contacts" in stats
