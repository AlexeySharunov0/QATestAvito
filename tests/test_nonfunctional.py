import time

import allure
import pytest

from api.models.avito.item_api import AvitoItemApi
from api.utils.client import AvitoApiClient


@allure.feature("Нефункциональные")
@pytest.mark.api
class TestPerformance(AvitoItemApi):
    """TC-401."""

    @allure.title("TC-401: Время ответа в допустимых пределах")
    def test_get_response_time(self, api_client, created_item):
        with allure.step("Получить id созданного объявления"):
            item_id = created_item["id"]
        with allure.step("Замерить время ответа GET item"):
            start = time.time()
            self.get_item(api_client, item_id)
            elapsed = time.time() - start
        with allure.step("Проверка: время ответа < 5 сек"):
            assert elapsed < 5, f"Ответ занял {elapsed:.2f}с, ожидалось < 5с"


@allure.feature("Нефункциональные")
@pytest.mark.api
class TestContentType(AvitoItemApi):
    """TC-402."""

    @allure.title("TC-402: Content-Type ответа — application/json")
    def test_content_type_json(self, api_client: AvitoApiClient, created_item):
        with allure.step("Получить id созданного объявления"):
            item_id = created_item["id"]
        with allure.step("Выполнить GET item и проверить заголовок Content-Type"):
            resp = api_client.get(f"item/{item_id}", raw=True)
            assert resp is not None
            ct = resp.headers.get("Content-Type", "")
            assert "application/json" in ct, f"Ожидался application/json, получено: {ct}"
