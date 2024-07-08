import json
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from src.utils import logging_setup, read_xlsx

logger = logging_setup()


def filter_transactions_by_category_and_date(pd_transactions: pd.DataFrame, category: str, begin_date: str) -> Any:
    """
    Фильтрация транзакций по категории и дате.

    Args:
        pd_transactions: DataFrame с транзакциями.
        category: Категория для фильтрации.
        begin_date: Дата начала 3-месячного периода в формате 'YYYY-MM-DD'.

    Returns:
        Список словарей с транзакциями, соответствующими запросу.
    """
    end_date = datetime.strptime(begin_date, "%d.%m.%Y") + timedelta(days=90)
    filtered_transactions = pd_transactions[
        (pd_transactions["category"] == category)
        & (pd_transactions["data_payment"] >= begin_date)
        & (pd_transactions["data_payment"] < end_date.strftime("d.%m.%Y"))
    ]
    return filtered_transactions.to_dict("records")


def main_of_reports() -> None:
    """
    Главная функция модуля.
    """
    operations = read_xlsx("../data/operations.xls")
    category = input("Введите категорию трат: ").capitalize()
    start_date = input("Введите дату начала 3-месячного периода (MM.DD.YYYY): ")

    # Convert the list of dictionaries to a pandas DataFrame
    pd_transactions = pd.DataFrame(operations)

    filtered_operations = filter_transactions_by_category_and_date(pd_transactions, category, start_date)

    with open("filtered_operations.json", "w", encoding="utf-8") as f:
        json.dump(filtered_operations, f, indent=4, ensure_ascii=False)

    logger.info("операции записаны в файл filtered_operations.json")
    print("операции записаны в файл filtered_operations.json")


if __name__ == "__main__":
    main_of_reports()
