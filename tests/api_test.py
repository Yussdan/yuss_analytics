"""
Тесты для API, включающие проверку получения последних данных о курсе BTC/USD
и получения исторических данных о курсе BTC за последние 5 дней.
"""
import requests

def test_get_latest(api_base_url):
    """
    Тест для получения последних данных о курсе BTC/USD.

    Отправляет GET-запрос к API, проверяет корректность статуса ответа,
    а также содержимое данных (тип данных и наличие информации о BTC).
    """
    response = requests.get(f'http://localhost:5000/latest/BTC/USD', timeout=20)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert 'BTC' in data

def test_get_history(api_base_url):
    """
    Тест для получения исторических данных о курсе BTC за последние 5 дней.

    Отправляет GET-запрос к API, проверяет статус ответа и содержимое данных.
    Убедится, что в ответе нет ошибок.
    """
    response = requests.get(f'http://localhost:5000/history/BTC/day/USD/5', timeout=20)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert 'error' not in data
