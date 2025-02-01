from fastapi import FastAPI
from app.routers import auth, user, todo

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)

@app.get("/")
def root():
    return {"message": "Todo app with API authentication"}
