from fastapi import FastAPI

from app.routers import bank_account

app = FastAPI(title="Bank Account API")
app.include_router(bank_account.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
