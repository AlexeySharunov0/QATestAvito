import allure
import pytest

from api.models.avito.item_api import AvitoItemApi, generate_item_data


@allure.feature("Негативные тесты")
@pytest.mark.api
class TestCreateNegative:
    """TC-101, TC-102, TC-103."""

    @allure.title("TC-101: Создание с пустым телом")
    def test_create_empty_body(self, api_client):
        with allure.step("Отправить POST с пустым телом, ожидать 400"):
            item_api = AvitoItemApi()
            item_api.create_item_400(api_client, {})

    @allure.title("TC-101: Создание без sellerID")
    def test_create_without_seller_id(self, api_client):
        with allure.step("Подготовка данных без sellerID и отправка, ожидать 400"):
            item_api = AvitoItemApi()
            data = generate_item_data()
            del data["sellerID"]
            item_api.create_item_400(api_client, data)

    @allure.title("TC-101: Создание без name")
    def test_create_without_name(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных без name и отправка, ожидать 400"):
            item_api = AvitoItemApi()
            data = generate_item_data(seller_id=unique_seller_id)
            del data["name"]
            item_api.create_item_400(api_client, data)

    @allure.title("TC-101: Создание без price")
    def test_create_without_price(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных без price и отправка, ожидать 400"):
            item_api = AvitoItemApi()
            data = generate_item_data(seller_id=unique_seller_id)
            del data["price"]
            item_api.create_item_400(api_client, data)

    @allure.title("TC-102: Создание с невалидным sellerID (строка)")
    def test_create_invalid_seller_id_string(self, api_client):
        with allure.step("Подготовка данных с sellerID=строка и отправка, ожидать 400"):
            item_api = AvitoItemApi()
            data = generate_item_data()
            data["sellerID"] = "not_a_number"
            item_api.create_item_400(api_client, data)

    @allure.title("TC-102: Создание с отрицательным sellerID")
    def test_create_negative_seller_id(self, api_client):
        with allure.step("Отправить данные с sellerID=-1, принять 200 или 400"):
            item_api = AvitoItemApi()
            data = generate_item_data(seller_id=-1)
            item_api.create_item(api_client, data, expected_status=[200, 400])

    @allure.title("TC-103: Создание с отрицательным price")
    def test_create_negative_price(self, api_client, unique_seller_id):
        with allure.step("Отправить данные с price=-100, принять 200 или 400"):
            item_api = AvitoItemApi()
            data = generate_item_data(seller_id=unique_seller_id, price=-100)
            item_api.create_item(api_client, data, expected_status=[200, 400])

    @allure.title("TC-103: Создание с невалидным типом price")
    def test_create_invalid_price_type(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных с price=строка и отправка, ожидать 400"):
            item_api = AvitoItemApi()
            data = generate_item_data(seller_id=unique_seller_id)
            data["price"] = "abc"
            item_api.create_item_400(api_client, data)


@allure.feature("Негативные тесты")
@pytest.mark.api
class TestGetItemNegative(AvitoItemApi):
    """TC-104, TC-105."""

    @allure.title("TC-104: Получение по несуществующему id")
    def test_get_nonexistent_id(self, api_client):
        with allure.step("Запросить объявление по несуществующему id, ожидать 400/404"):
            self.get_item(
                api_client,
                "00000000-0000-0000-0000-000000000001",
                expected_status=[400, 404],
            )

    @allure.title("TC-105: Получение с невалидным форматом id")
    def test_get_invalid_id(self, api_client):
        with allure.step("Запросить объявление с невалидным id, ожидать 400/404"):
            self.get_item(api_client, "invalid-id-format", expected_status=[400, 404])


@allure.feature("Негативные тесты")
@pytest.mark.api
class TestStatisticNegative(AvitoItemApi):
    """TC-106."""

    @allure.title("TC-106: Статистика по несуществующему объявлению")
    def test_statistic_nonexistent_id(self, api_client):
        with allure.step("Запросить статистику по несуществующему id, ожидать 400/404"):
            self.get_statistic(
                api_client,
                "00000000-0000-0000-0000-000000000001",
                expected_status=[400, 404],
            )


@allure.feature("Негативные тесты")
@pytest.mark.api
class TestGetBySellerNegative(AvitoItemApi):
    """TC-107."""

    @allure.title("TC-107: Получение с невалидным sellerId")
    def test_get_by_invalid_seller_id(self, api_client):
        with allure.step("Запросить объявления по sellerId=999999999, принять 200"):
            self.get_items_by_seller(api_client, 999999999, expected_status=200)
