from fastapi import FastAPI
from pydantic import BaseModel
import db.db_connection as db_interaction

class Book(BaseModel):
    ID: int
    title: str
    stock: int

#import os
#import json

app = FastAPI()

@app.get("/ping")
async def ping():
    output = "Pong"
    return output

# @app.get("/vcap")
# async def vcap():
#     vcap_services = os.getenv('VCAP_SERVICES')
#     vcap_services = json.loads(vcap_services)
#     return vcap_services

@app.get("/readData")
async def select_data():
    s_sql_select = """
        SELECT
            *
        FROM
            my_bookshop_Books;"""
    output = db_interaction.execute_sql(s_sql_select)
    return output
# Update stock of a book specified by the book_id with the provided stock value in the request body
@app.put("/updateStock/{book_id}")
async def update_stock(book_id: int, book: Book):
    s_sql_update = f"""
        UPDATE
            my_bookshop_Books
        SET
            stock = {book.stock}
        WHERE
            ID = {book_id};"""
    output = db_interaction.execute_sql(s_sql_update)
    return output

""" endpoint for health check """
@app.get("/health")
async def health():
    return {"status": "UP"}

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
