from fastapi import FastAPI

app = FastAPI()

@app.get("/dummy")
async def dummy():
    return None