from fastapi import FastAPI
from routers import tea, user, auth

app = FastAPI()

app.include_router(tea.router)
app.include_router(user.router)
app.include_router(auth.router)