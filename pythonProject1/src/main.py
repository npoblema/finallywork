from src.reports import main_of_reports
from src.services import main_of_services
from src.views import main_of_views


def main() -> None:
    """вызов всех функций"""
    main_of_views()
    main_of_reports()
    main_of_services()


if __name__ == "__main__":
    main()
