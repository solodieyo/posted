from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Start, Group, Select, Back, Row, SwitchTo, Calendar
from aiogram_dialog.widgets.text import Format, Const, Case

from app.src.bot.dialogs.common.buttons import BACK_TO_MANAGE_POST_MENU
from app.src.bot.dialogs.common.getters import (
	create_post_getter,
	channel_itemgetter,
	manage_menu_getter,
	get_post_delay_text,
	get_calendar_state,
	get_buttons_dates
)
from app.src.bot.dialogs.common.handlers import (
	on_notification_clicked,
	shift_left_date,
	shift_right_date,
	on_date_selected,
	on_show_calendar,
	on_no_confirm_user,
	on_confirm_delay_post, get_delay_confirm_info, on_delay_click
)
from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.dialogs.create_post_dialog.getters import (
	media_menu_getter,
	getter_channel_name
)
from app.src.bot.dialogs.create_post_dialog.handlers import (
	on_select_channel,
	input_post_text,
	input_post_media,
	on_hide_media,
	on_delete_media,
	input_url_buttons,
	input_emoji_buttons,
	input_time_delay,
	post_confirm,
)
from app.src.bot.states.dialog_states import CreatePostStates, AddChannelStates

create_main_menu = Window(
	I18NFormat(
		text='one-channel',
		when=F['one_channel'].is_(True)
	),
	I18NFormat(
		text='more-channels',
		when=F['one_channel'].is_(False)
	),
	Group(
		Select(
			text=Format('{item.channel_name}'),
			id='channel_select',
			items='channels',
			item_id_getter=channel_itemgetter,
			type_factory=int,
			on_click=on_select_channel
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
		func=input_post_text,
	),
	state=CreatePostStates.create_post,
	getter=create_post_getter
)

selected_channel_window = Window(
	I18NFormat(
		text='one-channel',
	),
	Back(
		text=Const('Выбрать другой канал')
	),
	MessageInput(
		func=input_post_text,
	),
	state=CreatePostStates.selected_channel,
	getter=getter_channel_name
)

post_manage_menu = Window(
	Format('{post_text}'),
	SwitchTo(
		text=Const('Изменить текст'),
		state=CreatePostStates.change_post_text,
		id='change_post_text'
	),
	SwitchTo(
		text=Const('Добавить медиа'),
		state=CreatePostStates.add_media,
		id='add_media'
	),
	Row(
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
			text=Const('URL-Кнопки'),
			id='url_buttons',
			state=CreatePostStates.url_buttons
		)
	),
	SwitchTo(
		text=Const('Добавить голосование'),
		id='add_poll',
		state=CreatePostStates.add_poll
	),
	SwitchTo(
		text=Const('Emoji-кнопки'),
		id='emoji_buttons',
		state=CreatePostStates.emoji_buttons
	),
	SwitchTo(
		text=Const('Далее ➡️'),
		id='pre_post_menu',
		state=CreatePostStates.post_final_menu
	),
	state=CreatePostStates.post_manage_menu,
	getter=manage_menu_getter
)

change_post_text = Window(
	Const('Отправьте новый текст для поста'),
	MessageInput(
		func=input_post_text,
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		id='__back__',
		state=CreatePostStates.post_manage_menu
	),
	state=CreatePostStates.change_post_text
)

add_media = Window(
	I18NFormat('add-media-text'),
	MessageInput(
		func=input_post_media,
	),
	Button(
		text=Case(
			{
				True: Const('✅ Скрывать медиа'),
				False: Const('❌ Скрывать медиа'),
			},
			selector='hide_media'
		),
		id='hide_media_button',
		on_click=on_hide_media
	),
	Button(
		text=Const('Удалить медиа'),
		id='delete_media_button',
		when='has_media',
		on_click=on_delete_media
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.add_media,
	getter=media_menu_getter
)

url_buttons = Window(
	I18NFormat('url-buttons-text'),
	MessageInput(
		func=input_url_buttons,
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.url_buttons,
	disable_web_page_preview=True
)

emoji_buttons = Window(
	I18NFormat('emoji-buttons-text'),
	MessageInput(
		func=input_emoji_buttons,
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.emoji_buttons
)


post_final_menu = Window(
	I18NFormat('post-final-text'),
	Row(
		SwitchTo(
			text=Const('Отложить'),
			id='post_delay',
			state=CreatePostStates.post_delay,
			on_click=on_delay_click
		),
		SwitchTo(
			text=Const('Опубликовать'),
			id='post_publish',
			state=CreatePostStates.confirm_post
		),
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.post_final_menu,
	getter=getter_channel_name
)

confirm_post = Window(
	Const('Вы уверены, что хотите опубликовать пост?'),
	Button(
		text=Const('✅ Опубликовать'),
		id='post_confirm',
		on_click=post_confirm
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		id='__back__',
		state=CreatePostStates.post_final_menu
	),
	state=CreatePostStates.confirm_post
)

delay_post_window = Window(
	Format(
		text='{post_delay_text}',
	),
	MessageInput(
		func=input_time_delay,
	),
	Row(
		Button(
			text=Format('←{left_date}'),
			id='left_date',
			on_click=shift_left_date
		),
		Button(
			text=Format('{current_date}'),
			id='current_date',
		),
		Button(
			text=Format('{right_date}→'),
			id='right_date',
			on_click=shift_right_date
		),
		when=F['show_calendar'].is_(True)
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
		state=CreatePostStates.post_final_menu
	),
	state=CreatePostStates.post_delay,
	getter=(
		get_post_delay_text,
		get_calendar_state,
		get_buttons_dates
	)
)

confirm_delay_post = Window(
	Format("Запланировать пост в канал {channel_name} на {selected_date}?"),
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
		state=CreatePostStates.post_delay,
		id='__back__to_time_delay__'
	),
	state=CreatePostStates.post_delay_confirm,
	getter=get_delay_confirm_info
)

create_post_dialog = Dialog(
	create_main_menu,
	post_manage_menu,
	selected_channel_window,
	change_post_text,
	add_media,
	url_buttons,
	emoji_buttons,
	post_final_menu,
	confirm_post,
	delay_post_window,
	confirm_delay_post
)
