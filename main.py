import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from views import router as view_router
from api import router as api_router

from infra.rabbit_depends import (
    init_broker,
    connect_broker,
    disconnect_broker,
)


# ------------------------------------------------------------------------------------
# Жизненный цикл приложения (lifespan) вместо on_event("startup") / on_event("shutdown")
# ------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    - до yield: код, выполняющийся "при старте" приложения
    - после yield: код, выполняющийся "при завершении" приложения
    """
    # ── startup ────────────────────────────────────
    init_broker(app)
    await connect_broker(app)

    yield

    # ── shutdown ───────────────────────────────────
    await disconnect_broker(app)


# ------------------------------------------------------------------------------------
# Инициализация приложения FastAPI с помощью lifespan + подключения
# ------------------------------------------------------------------------------------
app = FastAPI(
    title="QRS",
    lifespan=lifespan,
)
app.include_router(router=view_router)
app.include_router(router=api_router)


# ------------------------------------------------------------------------------------
# Точка входа
# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8008,
    )
