from fastapi import FastAPI

app = FastAPI(title="AccessVault")


@app.get("/")
def read_root():
    return {"message": "AccessVault API online"}
