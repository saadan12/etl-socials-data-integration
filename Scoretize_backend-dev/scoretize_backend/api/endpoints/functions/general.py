import datetime
import calendar


def get_int_list(list):
    if list:
        return [int(x) for x in list.split('-')]
    else:
        return None


def get_split_date(list):
    if list:
        year = list[0]
        month = list[1]
        day = list[2]
        return year, month, day
    else:
        return None


# NEW FUNCTIONSS


def start_date_values(start_date, end_date):
    if not end_date:
        end_date = current_day_noTime().strftime('%Y-%m-%d')
    if not start_date:
        date = datetime.datetime.strptime(
            end_date, '%Y-%m-%d') - datetime.timedelta(days=30)
        start_date = date.replace(
            day=calendar.monthrange(date.year, date.month)[1]
            ).date()
        if str(start_date) == str(end_date):
            date = datetime.datetime.strptime(
                end_date, '%Y-%m-%d') - datetime.timedelta(days=31)
        start_date = date.replace(
            day=calendar.monthrange(date.year, date.month)[1]
            ).date()
        return start_date
    return datetime.datetime.strptime(start_date, '%Y-%m-%d').date()


def start_date_simple(start_date):
    if not start_date:
        date = datetime.datetime.now() - datetime.timedelta(days=30)
        return date.replace(
            day=calendar.monthrange(date.year, date.month)[1]
            ).date()
    return datetime.datetime.strptime(start_date, '%Y-%m-%d').date()


def end_date_values(end_date):
    if not end_date:
        return current_day_noTime()
    else:
        return datetime.datetime.strptime(end_date, '%Y-%m-%d').date()


def date_minus_day(date):
    return date - datetime.timedelta(days=1)


def current_day_noTime():
    return datetime.datetime.now().date()
