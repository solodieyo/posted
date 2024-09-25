from datetime import date

from babel.dates import format_date


def get_delay_text(
	scheduled_text: str,
	post_date: date,
	count_post: int | str,
	wrong_date: bool
) -> str:
	if not wrong_date:
		tittle_text = f"""
	<b>ОТЛОЖИТЬ ПОСТ</b>

	Запланированных постов на {format_date(post_date, format='d MMMM YYYY г.', locale='ru')}
	 - <code>{count_post}</code>.

	{scheduled_text}
	Отправьте время выхода поста в вашем часовом поясе (GMT+5 Казахстан) в любом из предложенных форматов, например:
	"""
	else:
		tittle_text = "Некорректный формат времени. Отправьте, пожалуйста, время в корректном формате, например:"

	return (f"""
	{tittle_text}

<blockquote>"18:30",
"18 30",
"1830",
"18:30 04.08.2023",
"18:30 04.08"</blockquote>""")


def get_delay_poll_text(
	scheduled_text: str,
	post_date: date,
	count_post: int | str,
	wrong_date: bool
) -> str:
	if not wrong_date:
		tittle_text = f"""
	<b>ОТЛОЖИТЬ ГОЛОСОВАНИЕ</b>

	Запланированных голосований на {format_date(post_date, format='d MMMM YYYY г.', locale='ru')}
	 - <code>{count_post}</code>.

	{scheduled_text}
	Отправьте время выхода поста в вашем часовом поясе (GMT+5 Казахстан) в любом из предложенных форматов, например:
	"""
	else:
		tittle_text = "Некорректный формат времени. Отправьте, пожалуйста, время в корректном формате, например:"

	return (f"""
	{tittle_text}

<blockquote>"18:30",
"18 30",
"1830",
"18:30 04.08.2023",
"18:30 04.08"</blockquote>""")
