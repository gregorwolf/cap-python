from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
async def ping():
    output = "Pong"

    return output

""" endpoint for health check """
@app.get("/health")
async def health():
    return {"status": "UP"}

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
