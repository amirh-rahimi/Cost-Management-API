from fastapi import FastAPI
from app.costs.routs import router as router_cost
from app.users.auth import router as router_auth
from app.users.routs import router as router_user

app = FastAPI(title="Cost Management")

@app.get("/")
def root():
    return {"msg": "Wellcom"}

app.include_router(router_cost)
app.include_router(router_user)
app.include_router(router_auth)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",        # مسیر پکیجی اپ (نه app=app)
        host="0.0.0.0",        # یا 127.0.0.1 برای فقط لوکال
        port=8000,
        reload=True,           # فقط برای توسعه
        log_level="info",
    )