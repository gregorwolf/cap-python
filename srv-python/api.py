from fastapi import FastAPI
import db.db_connection as db_interaction

app = FastAPI()

@app.get("/ping")
async def ping():
    output = "Pong"
    return output

@app.get("/readData")
async def select_data():
    s_sql_select = """
        SELECT
            *
        FROM
            my_bookshop_Books;"""

    output = db_interaction.execute_sql(s_sql_select)

    return output

""" endpoint for health check """
@app.get("/health")
async def health():
    return {"status": "UP"}

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
