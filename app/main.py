from fastapi import FastAPI

app = FastAPI(
    title="Enigma Serverless AI API",
    description="Enigma is an AI powered workspace for academics and research porposes.",
    version="1.0.0"
)


app.add_api_routes(prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"Hello": "World"}