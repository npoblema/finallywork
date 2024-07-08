import json
import logging
from logging import Logger
from typing import Any

import pandas as pd


def logging_setup() -> Logger:
    """
    Настройка логирования.
    """
    # Настройка корневого логгера
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        filename="search_log.txt",
        filemode="w",
    )
    # Создание и возвращение объекта Logger
    logger = logging.getLogger(__name__)
    return logger


def read_xlsx(file_path: str) -> Any:
    """
    Эта функция читает данные о транзакциях из файла Excel.
    """
    try:
        transactions_df = pd.read_excel(file_path)
        return transactions_df.to_dict("records")  # Читаем файл Excel с помощью Pandas
    except FileNotFoundError:
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки


def write_json(file_path: str, data: Any) -> None:
    """Читает"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
