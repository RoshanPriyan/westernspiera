from fastapi import FastAPI
from users.router import router as user_router
from custom_middleware import ExceptionHandlerMiddleware

app = FastAPI()
app.include_router(user_router)

# middleware handled
app.add_middleware(ExceptionHandlerMiddleware)


@app.get("/")
async def health_check():
    return {"status": "ok"}
