MONTHS = [
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10, 'Outubro'),
    (11, 'Novembro'),
    (12, 'Dezembro'),
]


def get_last_day(year, month):
    import calendar
    from datetime import datetime
    # Get the month before
    month = month - 1
    if month == 0:
        month = 12
        # If the month return to 12, it means that
        # is from a year before.
        year -= 1
    day = calendar.monthrange(year, month)[1]
    return datetime(year, month, day).date()
