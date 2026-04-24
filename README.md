# Анализатор инвестиционных портфелей

Простой инструмент для анализа инвестиционных портфелей.

## Возможности

- Загрузка исторических данных о ценах акций
- Расчёт доходности портфеля
- Базовые метрики: доходность, волатильность, Sharpe ratio
- Анализ распределения активов

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```python
python main.py
```

## Пример

```python
from portfolio import Portfolio

# Создание портфеля
portfolio = Portfolio()
portfolio.add_asset('AAPL', shares=10)
portfolio.add_asset('GOOGL', shares=5)
portfolio.add_asset('MSFT', shares=8)

# Анализ
portfolio.analyze(period='1y')
portfolio.print_summary()
```

## Требования

- Python 3.8+
- pandas
- yfinance
- numpy
