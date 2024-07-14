import datetime

from reviews.exeptions import ValidationError


def validate_year(entered_year):
    if entered_year > datetime.datetime.now().year:
        raise ValidationError('f {entered_year} год ещё не наступил')
