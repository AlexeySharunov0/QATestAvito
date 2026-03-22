import allure
import pytest

from api.models.avito.item_api import AvitoItemApi, generate_item_data


@allure.feature("Создание объявления")
@allure.story("POST /api/1/item")
@pytest.mark.api
class TestCreateItem(AvitoItemApi):
    """TC-001, TC-002, TC-003, TC-201, TC-202, TC-203, TC-204, TC-205."""

    @allure.title("TC-001: Создание объявления с валидными данными")
    def test_create_with_valid_data(self, api_client, unique_seller_id):
        with allure.step("Подготовка валидных данных объявления"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                name="Test Item Valid",
                price=5000,
                likes=10,
                view_count=100,
                contacts=5,
            )
        with allure.step("Создание объявления через API"):
            response = self.create_item(api_client, data)
        with allure.step("Проверка ответа: id, sellerId, name, price, statistics"):
            assert "id" in response, "В ответе должен быть id"
            assert response["sellerId"] == unique_seller_id
            assert response["name"] == "Test Item Valid"
            assert response["price"] == 5000
            assert "statistics" in response
            assert response["statistics"]["likes"] == 10
            assert response["statistics"]["viewCount"] == 100
            assert response["statistics"]["contacts"] == 5

    @allure.title("TC-002: Создание с минимальными данными")
    def test_create_with_minimal_data(self, api_client, unique_seller_id):
        with allure.step("Подготовка минимальных данных"):
            data = generate_item_data(seller_id=unique_seller_id, price=1)
        with allure.step("Создание объявления"):
            response = self.create_item(api_client, data)
        with allure.step("Проверка id, sellerId, price"):
            assert "id" in response
            assert response["sellerId"] == unique_seller_id
            assert response["price"] == 1

    @allure.title("TC-003: Создание с минимальной статистикой")
    def test_create_with_minimal_statistics(self, api_client, unique_seller_id):
        """API требует likes, viewCount, contacts >= 1 (см. BUGS.md)."""
        with allure.step("Подготовка данных с минимальной статистикой"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                likes=1,
                view_count=1,
                contacts=1,
            )
        with allure.step("Создание объявления"):
            response = self.create_item(api_client, data)
        with allure.step("Проверка наличия id"):
            assert "id" in response

    @allure.title("TC-201: Идемпотентность — одинаковые данные дают разные id")
    def test_create_idempotency_different_ids(self, api_client, unique_seller_id):
        with allure.step("Подготовка одинаковых данных"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                name="Same Name",
                price=100,
            )
        with allure.step("Создание двух объявлений с одинаковыми данными"):
            r1 = self.create_item(api_client, data)
            r2 = self.create_item(api_client, data)
        with allure.step("Проверка: id разные, name и sellerId совпадают"):
            assert r1["id"] != r2["id"], "Каждое создание должно возвращать уникальный id"
            assert r1["name"] == r2["name"]
            assert r1["sellerId"] == r2["sellerId"]

    @allure.title("TC-202: Дублирование name, price, sellerId допускается")
    def test_duplicate_fields_allowed(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                name="Duplicate Name",
                price=999,
            )
        with allure.step("Создание двух объявлений"):
            r1 = self.create_item(api_client, data)
            r2 = self.create_item(api_client, data)
        with allure.step("Проверка: id разные, name совпадает"):
            assert r1["id"] != r2["id"]
            assert r1["name"] == r2["name"] == "Duplicate Name"

    @allure.title("TC-203: Создание с большими числовыми значениями")
    def test_create_with_large_values(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных с большими значениями"):
            data = generate_item_data(
                seller_id=unique_seller_id,
                price=999999999,
                likes=99999,
                view_count=99999,
                contacts=99999,
            )
        with allure.step("Создание объявления"):
            response = self.create_item(api_client, data)
        with allure.step("Проверка id и price"):
            assert "id" in response
            assert response["price"] == 999999999

    @allure.title("TC-204: Создание с длинным названием")
    def test_create_with_long_name(self, api_client, unique_seller_id):
        with allure.step("Подготовка данных с длинным названием (255 символов)"):
            long_name = "A" * 255
            data = generate_item_data(seller_id=unique_seller_id, name=long_name)
        with allure.step("Создание объявления"):
            response = self.create_item(api_client, data)
        with allure.step("Проверка id и сохранённого name"):
            assert "id" in response
            assert response["name"] == long_name

    @allure.title("TC-205: Создание со спецсимволами и Unicode в названии")
    @pytest.mark.parametrize(
        "name",
        [
            "Товар №1 <test>",
            "商品测试",
            "emoji 😀",
            "Café résumé",
        ],
    )
    def test_create_with_special_chars(self, api_client, unique_seller_id, name):
        with allure.step("Подготовка данных с спецсимволами/Unicode"):
            data = generate_item_data(seller_id=unique_seller_id, name=name)
        with allure.step("Создание объявления"):
            response = self.create_item(api_client, data)
        with allure.step("Проверка id и сохранённого name"):
            assert "id" in response
            assert response["name"] == name
