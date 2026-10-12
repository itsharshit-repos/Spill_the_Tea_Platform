from fastapi import FastAPI
from routers import tea, user

app = FastAPI()

app.include_router(tea.router)
app.include_router(user.router)