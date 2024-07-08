import json
from datetime import datetime
from typing import Optional

import pandas as pd

from src.utils import logging_setup

logger = logging_setup()


def transactions_by_keyword(search_term_2: str) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, содержащими search_term
    в описании или категории.

    Args:
        search_term_2: Строка для поиска.

    Returns:
        JSON-строка с результатами поиска.
    """
    logger.info(f"Поиск транзакций по ключевому слову: {search_term_2}")
    try:
        file_path = "../data/operations.xls"
        data = pd.read_excel(file_path)

        # Преобразование столбца 'description' и 'category' в строки
        data["description"] = data["description"].astype(str)
        data["category"] = data["category"].astype(str)

        # Фильтруем данные
        filtered_data = data[
            data["description"].str.contains(search_term_2, case=False)
            | data["category"].str.contains(search_term_2, case=False)
        ]

        # Преобразуем DataFrame в список словарей
        transaction_list = filtered_data.to_dict(orient="records")

        # Проверяем, пустой ли список
        if not transaction_list:
            transaction_list = [{"message": "Слово не найдено ни в одной категории"}]

        # Преобразуем список словарей в JSON-строку
        json_response = json.dumps(transaction_list, indent=4, ensure_ascii=False)

        # Записываем в файл
        with open("transactions_search_result.json", "w", encoding="utf-8") as f:
            json.dump(transaction_list, f, indent=4, ensure_ascii=False)

        logger.info("Результаты поиска записаны в файл transactions_search_result.json")
        return json_response

    except FileNotFoundError:
        logger.error("Файл operations.xls не найден.")
        return json.dumps({"error": "Файл operations.xls не найден."}, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        return json.dumps({"error": f"Произошла ошибка: {str(e)}"}, indent=4, ensure_ascii=False)


def expenses_by_category(transactions: pd.DataFrame, category: str, report_date: Optional[str] = None) -> str:
    """
    Вычисляет траты по категории за последние 3 месяца от указанной даты.

    Args:
        transactions: DataFrame с транзакциями.
        category: Категория для расчета.
        report_date: Дата, от которой отсчитывать 3 месяца.

    Returns:
        JSON-строка с результатами расчета.
    """
    # Если report_date предоставлен, преобразуем его в datetime, иначе используем текущую дату
    report_date_dt = datetime.strptime(report_date, "%Y-%m-%d") if report_date else datetime.now()

    logger.info(
        f"Расчет трат по категории: {category} за период  {report_date_dt - pd.DateOffset(months=3)}--{report_date_dt}"
    )
    # Преобразование столбца 'data_payment' в datetime с правильным форматом
    transactions["data_payment"] = pd.to_datetime(transactions["data_payment"], format="%d.%m.%Y")

    # Извлекаем нужные данные
    filtered_transactions = transactions[
        (transactions["category"] == category)
        & (transactions["data_payment"] >= report_date_dt - pd.DateOffset(months=3))
        & (transactions["data_payment"] <= report_date_dt)
    ]

    total_expenses = filtered_transactions["payment_amount"].sum()

    result = json.dumps(
        {"category": category, "total_expenses": total_expenses, "report_date": str(report_date_dt.date())},
        indent=4,
        ensure_ascii=False,
    )
    logger.info(f"Результаты расчета: {result}")
    return result


def main_of_services() -> None:
    """
    Основная функция модуля, которая обьединяет взаимодействие пользователя и функций
    """
    # Пример использования:
    print("Ведите слово для поиска например : Такси")
    search_term_1 = input()
    json_result = transactions_by_keyword(search_term_1)
    print(json_result)

    # Пример использования функции get_expenses_by_category
    transactions_df = pd.read_excel("../data/operations.xls")
    print("Ведите слово для поиска например : Ситидрайв")
    category_to_check = input()
    print("Ведите дату для поиска например : 2021-12-25")
    report_date_to_check = input()
    json_expenses_result = expenses_by_category(transactions_df, category_to_check, report_date_to_check)
    print(json_expenses_result)


if __name__ == "__main__":
    main_of_services()
