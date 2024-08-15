from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import uuid
import uvicorn
import logging


logging.basicConfig(level=logging.DEBUG)
app = FastAPI(
    title="URL Shortener APIS"
)

DATABASE_URL = "postgresql://shortener_user:shortener_password@localhost/url_shortener"


class URLRequest(BaseModel):
    url: str


async def get_database_connection():
    return await asyncpg.connect(DATABASE_URL)


@app.on_event("startup")
async def on_startup():
    conn = await get_database_connection()
    await conn.close()


@app.post("/shorten")
async def shorten_url(request: URLRequest):
    """
        get the shortened url
    """
    conn = await get_database_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    try:
        short_code = str(uuid.uuid4().hex[:6])
        await conn.execute(
            "INSERT INTO urls (short_code, original_url) VALUES ($1, $2)",
            f"http://localhost:8888/{short_code}", request.url
        )

        return {"short_url": f"http://localhost:8888/{short_code}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    finally:
        await conn.close()


@app.get("/{short_code}")
async def redirect_to_url(short_code: str):
    """
        get the original url from short code

        Args:

            short_code(str): short code of the original url we made above
    """
    conn = await get_database_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    row = await conn.fetchrow("SELECT original_url FROM urls WHERE short_code = $1", f"http://localhost:8888/{short_code}")
    if row:
        await conn.close()
        return {"redirect_url": row["original_url"]}
    else:
        await conn.close()
        raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")