import pytest

from api.utils.client import AvitoApiClient
from api.models.avito.item_api import AvitoItemApi, generate_item_data, generate_seller_id


@pytest.fixture
def api_client() -> AvitoApiClient:
    """HTTP-клиент для Avito API."""
    return AvitoApiClient()


@pytest.fixture
def unique_seller_id() -> int:
    """Уникальный sellerId для изоляции тестов (111111–999999)."""
    return generate_seller_id()


@pytest.fixture
def sample_item_data(unique_seller_id: int) -> dict:
    """Валидные данные для создания объявления."""
    return generate_item_data(seller_id=unique_seller_id)


@pytest.fixture
def created_item(api_client: AvitoApiClient, sample_item_data: dict) -> dict:
    """Создаёт объявление перед тестом, возвращает данные созданного объявления."""
    item_api = AvitoItemApi()
    response = item_api.create_item(api_client, sample_item_data)
    yield response
