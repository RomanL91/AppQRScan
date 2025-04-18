import uvicorn

from fastapi import FastAPI

from views import router as view_router
from api import router as api_router


app = FastAPI()
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
