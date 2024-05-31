from fastapi import FastAPI

from src.api.routers import all_routers

app = FastAPI(title="Student Tests App")


for router in all_routers:
    app.include_router(router)


