# MOEX ISS Python Client

Modern Python client for **Moscow Exchange ISS API**.

Проект предназначен для загрузки и обработки данных Московской биржи в задачах:

* quantitative trading
* backtesting
* machine learning
* feature engineering
* market research
* automated trading systems

Клиент предоставляет удобный интерфейс для работы с:

* историческими данными
* свечами
* рыночными данными
* инструментами MOEX
* futures и shares data

---

# Features

## Core

✅ Python 3.11+
✅ REST ISS API client
✅ Sync API (`requests`)
✅ Async API (`httpx`)
✅ Automatic pagination
✅ Retry mechanism
✅ Rate limiting
✅ JSON parsing
✅ Pandas integration
✅ Unit tests
✅ Mock HTTP testing

---

# Architecture

Проект построен как модульный клиент:

```
moex_iss/

├── client.py          # Основной ISS клиент
├── async_client.py    # Async версия
├── auth.py            # MOEX Passport authentication
├── session.py         # HTTP session layer
│
├── endpoints.py       # ISS URL builder
├── parser.py          # JSON parser
├── pagination.py      # start pagination
├── dataframe.py       # pandas adapters
│
├── limiter.py         # request rate limiter
├── models.py          # data models
├── exceptions.py      # custom exceptions
```

---

# Installation

## Clone repository

```bash
git clone <repository>

cd moex_iss
```

---

## Create virtual environment

Windows:

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install dependencies

Runtime:

```bash
pip install -r requirements.txt
```

Development:

```bash
pip install -r requirements-dev.txt
```

Install package:

```bash
pip install -e .
```

---

# Quick Start

## Basic client

```python
from moex_iss import ISSClient


client = ISSClient()


data = client.get(
    "/engines"
)


print(data)
```

---

# Historical data

Example: SBER history

```python
from moex_iss import ISSClient


client = ISSClient()


df = client.history_df(
    engine="stock",
    market="shares",
    board="TQBR",
    security="SBER",
    from_date="2025-01-01",
    till_date="2025-02-01"
)


print(df.head())
```

Result:

```
TRADEDATE     SECID     CLOSE     VOLUME

2025-01-01    SBER      250.5     100000
2025-01-02    SBER      252.0     120000
```

---

# Candles

Получение OHLCV данных:

```python
df = client.candles_df(
    security="SBER",
    interval=60
)
```

Result:

```
                     open high low close volume

2025-01-01 10:00     250  253 248 252   50000
```

Данные готовы для:

* indicators
* backtesting
* ML models

---

# Pagination

MOEX ISS ограничивает размер ответа.

Клиент автоматически обрабатывает:

```
start=0
start=100
start=200
...
```

Пример:

```python
for row in client.iter_history(
    engine="stock",
    market="shares",
    board="TQBR",
    security="GAZP"
):

    print(row)
```

Память не расходуется на загрузку всего датасета.

---

# Authentication

Для приватных данных:

```python
from moex_iss import ISSClient
from moex_iss import ISSConfig


config = ISSConfig(
    username="login",
    password="password"
)


client = ISSClient(
    config
)
```

Поддерживается:

* MOEX Passport
* cookie authentication
* session persistence

---

# Async API

Для параллельной загрузки:

```python
from moex_iss import AsyncISSClient


async with AsyncISSClient() as client:

    data = await client.get_json(
        "https://iss.moex.com/iss/engines.json"
    )
```

Использование:

* monitoring
* multiple instruments
* realtime polling

---

# Rate limiting

Для защиты от ограничения ISS:

```python
client = ISSClient(
    rate_limit=5
)
```

означает:

```
5 requests / second
```

---

# Error Handling

Клиент использует собственные исключения:

```python
from moex_iss.exceptions import (
    ISSServerError,
    ISSAuthenticationError,
    ISSRateLimitError
)
```

Пример:

```python
try:

    data = client.get_json(url)


except ISSServerError:

    reconnect()
```

---

# Testing

Запуск тестов:

```bash
pytest -v
```

---

Coverage:

```bash
pytest \
--cov=moex_iss \
--cov-report=term-missing
```

HTML отчет:

```bash
pytest \
--cov=moex_iss \
--cov-report=html
```

Открыть:

```
htmlcov/index.html
```

---

# Development

Code formatting:

```bash
black .
```

Lint:

```bash
ruff check .
```

Type checking:

```bash
mypy moex_iss
```

---

# Quant Pipeline Usage

Типичный workflow:

```
MOEX ISS

    |
    v

ISSClient

    |
    v

Pandas DataFrame

    |
    v

Feature Engineering

    |
    v

Model

    |
    v

Backtesting

    |
    v

Trading System
```

---

# Planned Features

## Market Data

* [ ] order book
* [ ] trades
* [ ] quotes

## Futures

* [ ] FORTS instruments
* [ ] futures candles
* [ ] open interest

## Analytics

* [ ] volatility indicators
* [ ] returns calculation
* [ ] technical indicators
* [ ] microstructure features

## Infrastructure

* [ ] parquet cache
* [ ] Redis cache
* [ ] Docker support
* [ ] CI/CD pipeline

---

# Requirements

Recommended:

```
Python >=3.11
```

Main dependencies:

```
requests
httpx
pandas
numpy
pydantic
tenacity
pytest
```

---

# License

MIT License

---

# Disclaimer

Проект предназначен для исследовательских и образовательных целей.

Перед использованием в реальной торговле необходимо учитывать:

* комиссии
* спреды
* проскальзывание
* ликвидность инструментов
* ограничения API
* рыночные режимы
* риск управления капиталом
