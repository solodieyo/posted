from operator import itemgetter

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Start, Group, Select, Back, Row, SwitchTo
from aiogram_dialog.widgets.text import Format, Const, Case

from app.src.bot.dialogs.add_channel_dialog.getters import create_post_getter, channel_itemgetter, manage_menu_getter, \
	media_menu_getter
from app.src.bot.dialogs.add_channel_dialog.handlers import on_select_channel, input_post_text, on_notification_clicked, \
	input_post_media, on_hide_media, on_delete_media
from app.src.bot.dialogs.common.buttons import BACK_TO_MANAGE_POST_MENU
from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.states.dialog_states import CreatePostStates

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
			text=Format('{item[1]}'),
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
		text=I18NFormat('add-channel'),
		state=CreatePostStates.add_channel,
		id='add_channel'
	),
	MessageInput(
		func=input_post_text,
	),
	state=CreatePostStates.create_post,
	getter=create_post_getter
)

selected_channel_window = Window(
	I18NFormat(
		text='selected-channel',
	),
	Back(
		text=Const('Выбрать другой канал')
	),
	MessageInput(
		func=input_post_text,
	),
	state=CreatePostStates.selected_channel
)

post_manage_menu = Window(
	Format('{post_text}'),
	Start(
		text=Const('Изменить текст'),
		state=CreatePostStates.change_post_text,
		id='change_post_text'
	),
	Start(
		text=Const('Добавить медиа'),
		state=CreatePostStates.add_media,
		id='add_media'
	),
	Row(
		Button(
			text=Case(
				texts={
					True: Const('🔔'),
					False: Const('🔕'),
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
	Start(
		text=Const('Добавить голосование'),
		id='add_poll',
		state=CreatePostStates.add_poll
	),
	Start(
		text=Const('Emoji-кнопки'),
		id='emoji_buttons',
		state=CreatePostStates.emoji_buttons
	),
	Start(
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
	BACK_TO_MANAGE_POST_MENU,
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
				True: Const('✅ Скрывать медиа'),встречался бы с ней?
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
	state=CreatePostStates.url_buttons
)

emoji_buttons = Window(
	I18NFormat('emoji-buttons-text'),
	MessageInput(
		func=input_emoji_buttons,
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.emoji_buttons
)


add_poll = Window(
	I18NFormat('add-poll-text'),
	MessageInput(
		func=input_poll_text,
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.add_poll
)

poll_choice_window = Window(
	I18NFormat('poll-choice-text'),
	MessageInput(
		func=input_poll_choice,
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.poll_choice
)


post_final_menu = Window(
	I18NFormat('post-final-text'),
	Row(
		Button(
			text=Const('Отложить'),
			id='post_delay',
			on_click=on_post_delay
		),
		SwitchTo(
			text=Const('Опубликовать'),
			id='post_publish',
			state=CreatePostStates.confirm_post
		),
	),
	BACK_TO_MANAGE_POST_MENU,
	state=CreatePostStates.post_final_menu
)

confirm_post = Window(
	Const('Вы уверены, что хотите опубликовать пост?'),
	Button(
		text=Const('✅ Опубликовать'),
		id='post_confirm'
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		id='__back__',
		state=CreatePostStates.post_final_menu
	),
	state=CreatePostStates.confirm_post
)

delay_post_window = Window(
	I18NFormat('delay-post-text'),
	MessageInput(
		func=input_time_delay,
	),
	SwitchTo(
		text=Const('⬅️ Назад'),
		id='__back__',
		state=CreatePostStates.post_final_menu
	),
	state=CreatePostStates.post_delay
)