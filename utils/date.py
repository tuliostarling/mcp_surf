from dateparser import parse


def resolve_date(text_date: str) -> str:
    """
    Convert natural language date expressions (like 'tomorrow', 'today', '3 de julho') into ISO format.

    Args:
        text_date (str): the natural language date expression.

    Returns:
        str: the resolved date in ISO format (YYYY-MM-DD), or original text if parsing fails.
    """
    dt = parse(text_date, languages=["pt", "en"])
    teste = dt.date().isoformat() if dt else text_date
    return teste
