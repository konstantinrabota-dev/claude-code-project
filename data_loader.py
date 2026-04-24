"""
Модуль для загрузки финансовых данных
"""
import yfinance as yf
import pandas as pd


class DataLoader:
    """Класс для загрузки данных о ценах активов"""

    def load_prices(self, tickers, period='1y', interval='1d'):
        """
        Загрузить исторические цены для списка тикеров

        Args:
            tickers (list): Список тикеров
            period (str): Период ('1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval (str): Интервал ('1d', '1wk', '1mo')

        Returns:
            pd.DataFrame: DataFrame с ценами закрытия
        """
        try:
            if len(tickers) == 1:
                data = yf.download(tickers[0], period=period, interval=interval, progress=False)
                if data.empty:
                    print(f"Не удалось загрузить данные для {tickers[0]}")
                    return None
                return pd.DataFrame({tickers[0]: data['Close']})
            else:
                data = yf.download(tickers, period=period, interval=interval, progress=False)
                if data.empty:
                    print("Не удалось загрузить данные")
                    return None
                return data['Close']
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return None

    def get_current_price(self, ticker):
        """
        Получить текущую цену актива

        Args:
            ticker (str): Тикер актива

        Returns:
            float: Текущая цена
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='1d')
            if data.empty:
                return None
            return data['Close'].iloc[-1]
        except Exception as e:
            print(f"Ошибка при получении цены {ticker}: {e}")
            return None

    def get_asset_info(self, ticker):
        """
        Получить информацию об активе

        Args:
            ticker (str): Тикер актива

        Returns:
            dict: Информация об активе
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            print(f"Ошибка при получении информации о {ticker}: {e}")
            return None
