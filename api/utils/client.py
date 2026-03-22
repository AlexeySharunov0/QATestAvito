from __future__ import annotations

import logging
from typing import Any

import requests
from requests import Response

from api.utils.routes import API_SERVICE, BASE_URL


class AvitoApiClient:
    """Базовый клиент для запросов к API объявлений."""

    def __init__(self, base_url: str = BASE_URL, service: str = API_SERVICE) -> None:
        self.base_url = base_url.rstrip("/")
        self.service = service.strip("/")
        self.logger = logging.getLogger(__name__)
        self._timeout = 15

    def _build_url(self, endpoint: str) -> str:
        """Собирает полный URL из base_url, service и endpoint."""
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{self.service}/{endpoint}"

    def _request(
        self,
        method: str,
        endpoint: str,
        expected_status_codes: int | list[int],
        **kwargs: Any,
    ) -> Response:
        """Выполняет HTTP-запрос и проверяет код ответа."""
        url = self._build_url(endpoint)
        headers = kwargs.pop("headers", {})
        headers.setdefault("Accept", "application/json")
        if "json" in kwargs:
            headers.setdefault("Content-Type", "application/json")

        self.logger.info("Запрос: %s %s, ожидаемый статус: %s", method, url, expected_status_codes)
        response = requests.request(
            method,
            url,
            headers=headers,
            timeout=self._timeout,
            **kwargs,
        )
        response.encoding = "utf-8"

        if isinstance(expected_status_codes, int):
            expected_status_codes = [expected_status_codes]
        assert response.status_code in expected_status_codes, (
            f"Ожидался статус {expected_status_codes}, получен {response.status_code}. "
            f"Тело ответа: {response.text[:500]}"
        )
        return response

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        expected_status_code: int | list[int] = 200,
        raw: bool = False,
    ) -> dict[str, Any] | list[Any] | Response:
        """GET-запрос."""
        response = self._request(
            "GET",
            endpoint,
            expected_status_codes=expected_status_code,
            params=params,
        )
        return response if raw else response.json()

    def post(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        expected_status_code: int | list[int] = 200,
        raw: bool = False,
    ) -> dict[str, Any] | Response:
        """POST-запрос."""
        response = self._request(
            "POST",
            endpoint,
            expected_status_codes=expected_status_code,
            json=json,
        )
        return response if raw else response.json()
