from datetime import date, datetime

FORMATS = [
	"%H:%M",
	"%H %M",
	"%H%M",
	"%H:%M %d.%m.%Y",
	"%H:%M %d.%m"
]


def parse_user_time(default_date: date, time_string: str) -> date | None:
	for fmt in FORMATS:
		try:
			parsed_datetime = datetime.strptime(time_string, fmt)
			if "%d.%m.%Y" in fmt or "%d.%m" in fmt:
				return parsed_datetime
			else:
				return datetime.combine(default_date, parsed_datetime.time())
		except ValueError:
			continue

	return None
