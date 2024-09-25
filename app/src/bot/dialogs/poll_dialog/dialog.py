from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Select, Start, Back, SwitchTo, Button, Row, Calendar
from aiogram_dialog.widgets.text import Format, Const, Case

from app.src.bot.dialogs.common.buttons import BACK_TO_MANAGE_POLL_MENU
from app.src.bot.dialogs.common.getters import (
	create_post_getter,
	channel_itemgetter,
	get_post_delay_text,
	get_calendar_state,
	get_buttons_dates
)
from app.src.bot.dialogs.common.handlers import (
	on_notification_clicked,
	shift_left_date,
	shift_right_date,
	on_show_calendar,
	on_date_selected,
	on_no_confirm_user,
	on_confirm_delay_post,
	get_delay_confirm_info, on_delay_click
)
from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.dialogs.create_post_dialog.getters import getter_channel_name
from app.src.bot.dialogs.poll_dialog.getters import getter_poll_choices
from app.src.bot.dialogs.poll_dialog.handlers import (
	on_select_channel_poll,
	input_poll_choices,
	change_poll_tittle,
	input_tittle_text,
	poll_confirm,
	input_poll_time_delay
)
from app.src.bot.states.dialog_states import AddChannelStates, PollStates

create_main_menu = Window(
	I18NFormat(
		text='one-channel-poll',
		when=F['one_channel'].is_(True)
	),
	I18NFormat(
		text='more-channels-poll',
		when=F['one_channel'].is_(False)
	),
	Group(
		Select(
			text=Format('{item.channel_name}'),
			id='channel_select',
			items='channels',
			item_id_getter=channel_itemgetter,
			type_factory=int,
			on_click=on_select_channel_poll
		),
		width=2,
		when=F['one_channel'].is_(False)
	),
	Start(
		text=Const(" ➕ Добавить новый канал"),
		state=AddChannelStates.add_channel,
		id='add_channel',
	),
	MessageInput(
		func=input_tittle_text,
	),
	state=PollStates.main,
	getter=create_post_getter
)

selected_channel_window = Window(
	I18NFormat(
		text='one-channel-poll',
	),
	Back(
		text=Const('Выбрать другой канал')
	),
	MessageInput(
		func=input_tittle_text,
	),
	state=PollStates.selected_channel,
	getter=getter_channel_name
)


poll_manage_menu = Window(
	Format('Заголовок голосования - {poll_tittle}\n\nВыборы голосования - {poll_choices}'),
	SwitchTo(
		text=Const('Изменить текст'),
		state=PollStates.change_poll_tittle,
		id='change_poll_tittle'
	),
	SwitchTo(
		text=Const('Изменить выборы'),
		state=PollStates.change_poll_choices,
		id='chane_poll_choices'
	),
	Button(
		text=Case(
			texts={
				False: Const('🔔'),
				True: Const('🔕'),
			},
			selector='notification'
		),
		id='notification_choice',
		on_click=on_notification_clicked
	),
	SwitchTo(
		text=Const('Далее ➡️'),
		id='pre_post_menu',
		state=PollStates.poll_final_menu
	),
	state=PollStates.poll_manage_menu,
	getter=getter_poll_choices
)


add_poll = Window(
	I18NFormat('add-poll-text'),
	MessageInput(
		func=change_poll_tittle,
	),
	BACK_TO_MANAGE_POLL_MENU,
	state=PollStates.change_poll_tittle
)

poll_choice_window = Window(
	I18NFormat('poll-choice-text'),
	MessageInput(
		func=input_poll_choices,
	),
	BACK_TO_MANAGE_POLL_MENU,
	state=PollStates.change_poll_choices
)


post_final_menu = Window(
	I18NFormat('poll-final-text'),
	Row(
		SwitchTo(
			text=Const('Отложить'),
			id='post_delay',
			state=PollStates.poll_delay,
			on_click=on_delay_click
		),
		SwitchTo(
			text=Const('Опубликовать'),
			id='post_publish',
			state=PollStates.poll_confirm
		),
	),
	BACK_TO_MANAGE_POLL_MENU,
	state=PollStates.poll_final_menu,
	getter=getter_channel_name
)


confirm_post = Window(
	Const('Вы уверены, что хотите опубликовать голосование?'),
	Button(
		text=Const('✅ Опубликовать'),
		id='post_confirm',
		on_click=poll_confirm
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		id='__back__',
		state=PollStates.poll_final_menu
	),
	state=PollStates.poll_confirm
)

delay_post_window = Window(
	Format(
		text='{post_delay_text}',
	),
	MessageInput(
		func=input_poll_time_delay,
	),
	Row(
		Button(
			text=Format('←{left_date}'),
			id='left_date',
			on_click=shift_left_date
		),
		Button(
			text=Format('←{current_date}'),
			id='current_date',
		),
		Button(
			text=Format('←{right_date}'),
			id='right_date',
			on_click=shift_right_date
		),
		when=F['show_calendar'].is_(False)
	),
	Button(
		text=Case(
			{
				True: Const('Показать календарь'),
				False: Const('Скрыть календарь'),
			},
			selector='show_calendar'
		),
		id='hide_calendar',
		on_click=on_show_calendar
	),
	Calendar(
		id='calendar',
		on_click=on_date_selected,
		when=F['show_calendar'].is_(False)
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		id='__back__',
		state=PollStates.poll_final_menu
	),
	state=PollStates.poll_delay,
	getter=(
		get_post_delay_text,
		get_calendar_state,
		get_buttons_dates
	)
)

confirm_delay_poll = Window(
	Format("Запланировать голосование в канал {channel_name} на {selected_date}?"),
	Button(
		text=Const('Да запланировать'),
		id='confirm_delay_post',
		on_click=on_confirm_delay_post
	),
	Button(
		text=Case(
			{
				False: Const('Больше не спрашивать'),
				True: Const('Спрашивать подтверждение'),
			},
			selector='user_confirm'
		),
		id='no_confirm_delay_ask',
		on_click=on_no_confirm_user
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		state=PollStates.poll_delay,
		id='__back__to_time_delay__'
	),
	state=PollStates.poll_delay_confirm,
	getter=get_delay_confirm_info
)

poll_dialog = Dialog(
	create_main_menu,
	selected_channel_window,
	poll_manage_menu,
	add_poll,
	poll_choice_window,
	confirm_post,
	delay_post_window,
	confirm_delay_poll,
	post_final_menu
)