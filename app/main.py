from fastapi import FastAPI
from app.costs.routs import router

app = FastAPI(title="Cost Management")

@app.get("/")
def root():
    return {"msg": "Wellcom"}

app.include_router(router)
