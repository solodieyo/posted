from aiogram import Router

from .create import router as create_router
from .start import router as start_router


def setup_routers():
	router = Router()
	router.include_routers(
		start_router,
		create_router,
	)
	return router