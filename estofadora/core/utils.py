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


def last_day_of(year, month):
    '''
        Retun the last day of the year/month given.
    '''
    import calendar
    from datetime import datetime

    day = calendar.monthrange(year, month)[1]
    return datetime(year, month, day).date()


def month_before_of(year, month):
    '''
        Retun the before month of the year/month given.
    '''
    # Get the month before
    month = month - 1
    if month == 0:
        # If was January, should return to December.
        month = 12
        # If the month return to December, it means that
        # is from a year before.
        year -= 1
    return year, month
