import unittest
from io import StringIO
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd

# Импортируем функции, которые мы будем тестировать
from src.reports import main_of_reports, read_xlsx


class TestReadTransactionsXlsx(unittest.TestCase):
    @patch("pandas.read_excel")
    def test_read_transactions_xlsx_success(self, mock_read_excel: Any) -> None:
        # Создаем мок DataFrame
        mock_df = pd.DataFrame(
            {"category": ["Food", "Utilities"], "data_payment": ["01.01.2020", "02.01.2020"], "amount": [100, 200]}
        )
        mock_read_excel.return_value = mock_df

        # Вызываем функцию
        result = read_xlsx("dummy_path.xlsx")

        # Проверяем результат
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_read_transactions_xlsx_failure(self, mock_read_excel: Any) -> None:
        # Вызываем функцию
        result = read_xlsx("nonexistent_path.xlsx")

        # Проверяем, что результат - пустой DataFrame
        self.assertTrue(result.empty)


class TestMainReports(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("src.reports.filter_transactions_by_category_and_date")
    @patch("src.reports.read_transactions_xlsx")
    @patch("sys.stdin", StringIO("Food\n01.01.2020\n"))
    def test_main_reports(
        self, mock_read_transactions_xlsx: Any, mock_filter_transactions_by_category_and_date: Any, mock_open: Any
    ) -> None:
        # Настраиваем моки
        mock_df = pd.DataFrame()
        mock_read_transactions_xlsx.return_value = mock_df
        mock_filter_transactions_by_category_and_date.return_value = []

        # Вызываем функцию
        main_of_reports()

        # Проверяем, что функции были вызваны с правильными аргументами
        mock_read_transactions_xlsx.assert_called_once_with("../data/operations_mi.xls")
        mock_filter_transactions_by_category_and_date.assert_called_once_with(mock_df, "Food", "01.01.2020")


if __name__ == "__main__":
    unittest.main()
