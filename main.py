"""
Пример использования анализатора портфелей
"""
import sys
import io

# Устанавливаем UTF-8 для корректного вывода в Windows консоль
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from portfolio import Portfolio


def main():
    print("=" * 60)
    print("АНАЛИЗАТОР ИНВЕСТИЦИОННЫХ ПОРТФЕЛЕЙ")
    print("=" * 60)

    # Создаём портфель
    portfolio = Portfolio()

    # Добавляем активы (примеры популярных акций)
    print("\nДобавление активов в портфель:")
    portfolio.add_asset('AAPL', shares=10)   # Apple
    portfolio.add_asset('GOOGL', shares=5)   # Google
    portfolio.add_asset('MSFT', shares=8)    # Microsoft
    portfolio.add_asset('TSLA', shares=3)    # Tesla

    # Анализируем портфель за последний год
    print("\nЗапуск анализа портфеля...")
    portfolio.analyze(period='1y')

    # Выводим результаты
    portfolio.print_summary()

    # Показываем распределение активов
    portfolio.get_asset_allocation()


if __name__ == "__main__":
    main()
