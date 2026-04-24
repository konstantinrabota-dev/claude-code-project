"""
Модуль для аналитики портфеля
"""
import numpy as np
import pandas as pd


class Analytics:
    """Класс для расчёта финансовых метрик"""

    def calculate_returns(self, prices):
        """
        Рассчитать доходность

        Args:
            prices (pd.Series): Временной ряд цен

        Returns:
            pd.Series: Доходность
        """
        return prices.pct_change().dropna()

    def calculate_volatility(self, returns, annualize=True):
        """
        Рассчитать волатильность

        Args:
            returns (pd.Series): Доходность
            annualize (bool): Аннуализировать результат

        Returns:
            float: Волатильность в процентах
        """
        vol = returns.std()
        if annualize:
            vol = vol * np.sqrt(252)  # 252 торговых дня в году
        return vol * 100

    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """
        Рассчитать коэффициент Шарпа

        Args:
            returns (pd.Series): Доходность
            risk_free_rate (float): Безрисковая ставка (годовая)

        Returns:
            float: Коэффициент Шарпа
        """
        excess_returns = returns - (risk_free_rate / 252)
        if excess_returns.std() == 0:
            return 0
        sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
        return sharpe

    def calculate_max_drawdown(self, prices):
        """
        Рассчитать максимальную просадку

        Args:
            prices (pd.Series): Временной ряд цен/стоимости

        Returns:
            tuple: (максимальная просадка в валюте, максимальная просадка в %)
        """
        cumulative_max = prices.expanding().max()
        drawdown = prices - cumulative_max
        max_dd = drawdown.min()
        max_dd_pct = (max_dd / cumulative_max[drawdown.idxmin()]) * 100
        return max_dd, max_dd_pct

    def calculate_cagr(self, initial_value, final_value, years):
        """
        Рассчитать среднегодовой темп роста (CAGR)

        Args:
            initial_value (float): Начальная стоимость
            final_value (float): Конечная стоимость
            years (float): Количество лет

        Returns:
            float: CAGR в процентах
        """
        if years == 0 or initial_value == 0:
            return 0
        cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
        return cagr

    def calculate_correlation_matrix(self, returns_df):
        """
        Рассчитать корреляционную матрицу для нескольких активов

        Args:
            returns_df (pd.DataFrame): DataFrame с доходностями активов

        Returns:
            pd.DataFrame: Корреляционная матрица
        """
        return returns_df.corr()
