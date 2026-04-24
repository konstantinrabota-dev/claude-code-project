"""
Модуль для работы с инвестиционным портфелем
"""
import pandas as pd
import numpy as np
from data_loader import DataLoader
from analytics import Analytics


class Portfolio:
    """Класс для управления инвестиционным портфелем"""

    def __init__(self):
        self.assets = {}
        self.data_loader = DataLoader()
        self.analytics = Analytics()
        self.price_data = None
        self.portfolio_value = None

    def add_asset(self, ticker, shares):
        """
        Добавить актив в портфель

        Args:
            ticker (str): Тикер актива (например, 'AAPL')
            shares (int/float): Количество акций
        """
        self.assets[ticker] = shares
        print(f"Добавлен актив: {ticker} ({shares} шт.)")

    def remove_asset(self, ticker):
        """Удалить актив из портфеля"""
        if ticker in self.assets:
            del self.assets[ticker]
            print(f"Удалён актив: {ticker}")
        else:
            print(f"Актив {ticker} не найден в портфеле")

    def load_data(self, period='1y', interval='1d'):
        """
        Загрузить исторические данные для всех активов

        Args:
            period (str): Период данных ('1mo', '3mo', '6mo', '1y', '2y', '5y')
            interval (str): Интервал данных ('1d', '1wk', '1mo')
        """
        if not self.assets:
            print("Портфель пуст. Добавьте активы.")
            return

        print(f"\nЗагрузка данных за период: {period}")
        tickers = list(self.assets.keys())
        self.price_data = self.data_loader.load_prices(tickers, period, interval)

        if self.price_data is not None:
            print(f"Данные загружены: {len(self.price_data)} записей")

    def calculate_portfolio_value(self):
        """Рассчитать стоимость портфеля во времени"""
        if self.price_data is None:
            print("Сначала загрузите данные методом load_data()")
            return None

        portfolio_value = pd.Series(0, index=self.price_data.index)

        for ticker, shares in self.assets.items():
            if ticker in self.price_data.columns:
                portfolio_value += self.price_data[ticker] * shares

        self.portfolio_value = portfolio_value
        return portfolio_value

    def analyze(self, period='1y'):
        """
        Провести полный анализ портфеля

        Args:
            period (str): Период для анализа
        """
        self.load_data(period)

        if self.price_data is None:
            return

        self.calculate_portfolio_value()

    def print_summary(self):
        """Вывести сводку по портфелю"""
        if self.portfolio_value is None:
            print("Сначала выполните analyze()")
            return

        print("\n" + "="*60)
        print("АНАЛИЗ ПОРТФЕЛЯ")
        print("="*60)

        print("\nСостав портфеля:")
        for ticker, shares in self.assets.items():
            if ticker in self.price_data.columns:
                current_price = self.price_data[ticker].iloc[-1]
                value = current_price * shares
                print(f"  {ticker}: {shares} шт. * ${current_price:.2f} = ${value:.2f}")

        initial_value = self.portfolio_value.iloc[0]
        final_value = self.portfolio_value.iloc[-1]
        total_return = ((final_value - initial_value) / initial_value) * 100

        print(f"\nНачальная стоимость: ${initial_value:.2f}")
        print(f"Текущая стоимость: ${final_value:.2f}")
        print(f"Общая доходность: {total_return:.2f}%")

        returns = self.analytics.calculate_returns(self.portfolio_value)
        volatility = self.analytics.calculate_volatility(returns)
        sharpe = self.analytics.calculate_sharpe_ratio(returns)

        print(f"\nВолатильность (годовая): {volatility:.2f}%")
        print(f"Коэффициент Шарпа: {sharpe:.2f}")

        max_dd, max_dd_pct = self.analytics.calculate_max_drawdown(self.portfolio_value)
        print(f"Максимальная просадка: ${max_dd:.2f} ({max_dd_pct:.2f}%)")

        print("="*60 + "\n")

    def get_asset_allocation(self):
        """Получить распределение активов в портфеле"""
        if self.price_data is None:
            print("Сначала загрузите данные")
            return None

        allocation = {}
        total_value = 0

        for ticker, shares in self.assets.items():
            if ticker in self.price_data.columns:
                current_price = self.price_data[ticker].iloc[-1]
                value = current_price * shares
                allocation[ticker] = value
                total_value += value

        allocation_pct = {k: (v/total_value)*100 for k, v in allocation.items()}

        print("\nРаспределение активов:")
        for ticker, pct in allocation_pct.items():
            print(f"  {ticker}: {pct:.2f}%")

        return allocation_pct
