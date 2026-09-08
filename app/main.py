from fastapi import FastAPI
from cost.routs import router

app = FastAPI(title="Cost Management")

@app.get("/")
def root():
    return {"msg": "Wellcom"}

app.include_router(router)
