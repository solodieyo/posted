from datetime import datetime, date
import pytz

# Пример форматов
FORMATS = [
    "%H:%M",        # Время в формате HH:MM
    "%H%M",         # Время в формате HHMM (например, 1705)
    "%d.%m.%Y %H:%M",  # Полная дата и время
    "%d.%m.%Y"      # Только дата
]

# Временная зона Москвы
moscow_tz = pytz.timezone('Europe/Moscow')

def parse_user_time(default_date: datetime, time_string: str) -> datetime | None:
    for fmt in FORMATS:
        try:
            parsed_datetime = datetime.strptime(time_string, fmt)
            # Если строка содержит дату, вернём полный объект datetime с временной зоной
            if "%d.%m.%Y" in fmt or "%d.%m" in fmt:
                return moscow_tz.localize(parsed_datetime)
            else:
                # Комбинируем дату и время, и добавляем временную зону через localize
                result = datetime.combine(default_date.date(), parsed_datetime.time())
                result = moscow_tz.localize(result)
                print(result, 2)  # Для отладки
                return result
        except ValueError:
            continue

    return None

# Пример использования
default_date = datetime(2024, 9, 25, 17, 2, 9, 563544, tzinfo=pytz.timezone('Europe/Moscow'))
time_string = "1705"  # Время в формате HHMM
parsed_time = parse_user_time(default_date, time_string)

print(parsed_time)
result = parsed_time.isoformat()
print(datetime.fromisoformat(result))