"""Connect and Write to DB"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
async def select_data():
    output = "Pong"

    return output

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
