from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
	main_menu = State()


class CreatePostStates(StatesGroup):
	create_post = State()
	selected_channel = State()
	add_channel = State()
	post_manage_menu = State()
	change_post_text = State()
	add_media = State()
	add_poll = State()
	emoji_buttons = State()
	post_final_menu = State()
	url_buttons = State()
	poll_choice = State()
	confirm_post = State()
	post_delay = State()
	post_delay_confirm = State()


class AddChannelStates(StatesGroup):
	no_channel_yet = State()
	add_channel = State()
	channel_linked = State()


class PollStates(StatesGroup):
	main = State()
	selected_channel = State()
	add_poll = State()
	input_choices = State()
	poll_final_menu = State()
	poll_confirm = State()
	poll_delay = State()
	change_poll_tittle = State()
	change_poll_choices = State()
	poll_manage_menu = State()
	poll_delay_confirm = State()