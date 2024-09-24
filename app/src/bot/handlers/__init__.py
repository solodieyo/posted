from aiogram import Router

from .create import router as create_router
from .start import router as start_router
from .callback.reaction import router as reaction_router


def setup_routers():
	router = Router()
	router.include_routers(
		start_router,
		create_router,
		reaction_router
	)
	return router