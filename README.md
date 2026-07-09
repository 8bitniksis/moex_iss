# MOEX ISS Python Client

[![CI](https://github.com/8bitniksis/moex_iss/actions/workflows/ci.yml/badge.svg)](https://github.com/8bitniksis/moex_iss/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-black)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type%20checked-mypy-blue)](https://mypy-lang.org/)

Modern Python client for **Moscow Exchange ISS API**.

Проект предназначен для загрузки, хранения и анализа данных Московской биржи в задачах:

* quantitative trading
* backtesting
* machine learning
* feature engineering
* market research
* automated trading systems

Клиент предоставляет удобный интерфейс для работы с:

* историческими данными
* OHLCV свечами
* рыночными данными
* инструментами MOEX
* shares
* futures
* research datasets

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
✅ Parquet export  
✅ Unit tests  
✅ Mock HTTP testing  

---

# Architecture

Проект построен как модульный Python клиент:

```

moex_iss/

├── client.py          # Основной ISS клиент
├── async_client.py    # Async версия клиента
├── auth.py            # MOEX Passport authentication
├── session.py         # HTTP session layer
│
├── endpoints.py       # ISS URL builder
├── parser.py          # JSON parser
├── pagination.py      # Pagination logic
├── dataframe.py       # Pandas adapters
│
├── limiter.py         # Request rate limiter
├── models.py          # Data models
├── exceptions.py      # Custom exceptions

```

---

# Installation

## Clone repository

```bash
git clone <repository>

cd moex_iss
````

---

## Create virtual environment

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Install dependencies

Runtime:

```bash
pip install -r requirements.txt
```

Development:

```bash
pip install -r requirements-dev.txt
```

Quant research:

```bash
pip install -r requirements-quant.txt
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

# Historical Data

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

Example:

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

Поддерживаемые интервалы:

```
1    minute
10   minutes
60   minutes
24   daily
```

Result:

```
                     open high low close volume

2025-01-01 10:00     250  253 248 252   50000
```

Данные готовы для:

* indicators
* feature engineering
* machine learning
* backtesting

---

# MOEX ISS Endpoints

Пример корректных endpoint:

Engines:

```
https://iss.moex.com/iss/engines.json
```

Markets:

```
https://iss.moex.com/iss/engines/stock/markets.json
```

Candles:

```
https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/SBER/candles.json
```

Важно:

```
/iss/markets.json
```

не является существующим ISS endpoint.

---

# Pagination

MOEX ISS ограничивает размер ответа.

Клиент автоматически поддерживает:

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

Большие датасеты загружаются без переполнения памяти.

---

# Parquet Export

Для хранения исторических данных используется формат Parquet.

Требуется:

```
pyarrow
```

Пример:

```python
from pathlib import Path

from moex_iss import ISSClient


Path("data").mkdir(
    exist_ok=True
)


client = ISSClient()


df = client.candles_df(
    "SBER",
    interval=10
)


df.to_parquet(
    "data/sber_10m.parquet"
)
```

Результат:

```
data/

└── sber_10m.parquet
```

Чтение:

```python
import pandas as pd


df = pd.read_parquet(
    "data/sber_10m.parquet"
)
```

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

* multiple instruments
* monitoring
* batch download
* realtime polling

---

# Rate Limiting

Защита от ограничения MOEX ISS:

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

# Examples

```
examples/

├── 03_get_candles.py
├── 06_async_download.py
└── 07_export_parquet.py
```

Запуск:

```bash
python examples/03_get_candles.py
```

или:

```bash
python examples/07_export_parquet.py
```

---

# Testing

Запуск:

```bash
pytest -v
```

Coverage:

```bash
pytest \
--cov=moex_iss \
--cov-report=term-missing
```

HTML:

```bash
pytest \
--cov=moex_iss \
--cov-report=html
```

---

# Development

Formatting:

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

# Quant Pipeline

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

Parquet Storage

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

* [x] parquet export
* [ ] parquet cache layer
* [ ] incremental updates
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
pyarrow
pydantic
tenacity
```

---

# License

Apache License 2.0

Copyright (c) 2026

Licensed under the Apache License, Version 2.0.

You may obtain a copy of the License at:

```
https://www.apache.org/licenses/LICENSE-2.0
```

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
