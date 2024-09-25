from enum import StrEnum, auto


class MessageType(StrEnum):
	poll = auto()
	message = auto()