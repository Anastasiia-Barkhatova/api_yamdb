import datetime


def validate_year(entered_year):
    if entered_year > datetime.datetime.now().year:
        raise 'f {} год ещё не наступил'
