# Лабораторная работа №24 задание 1. Коритко Артур

from datetime import datetime
import time


def countdown_to_new_year():
    while True:
        now = datetime.now()
        new_year = datetime(year=now.year + 1, month=1, day=1)
        remaining = new_year - now
        print(f"\rДо Нового года: {remaining.days} дней, {remaining.seconds // 3600} час, "
              f"{(remaining.seconds % 3600) // 60} минут, {remaining.seconds % 60} секунд", end="")
        time.sleep(1)


countdown_to_new_year()


# Лабораторная работа №24 задание 2. Коритко Артур


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


current_year = datetime.now().year

if is_leap_year(current_year):
    print(f"{current_year} год высокосный")
else:
    print(f"{current_year} год не высокосный")


# Лабораторная работа №24 задание 3. Коритко Артур


def get_day_of_week():
    date_str = input("Введите дату в формате ДД.ММ.ГГГГ: ")
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y")
        days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        print(f"День недели: {days[date.weekday()]}")
    except ValueError:
        print("Не правильный формат даты")


get_day_of_week()
