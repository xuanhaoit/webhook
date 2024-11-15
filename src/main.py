from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from datetime import datetime
import logging
import os

load_dotenv()
max_msg = os.getenv("MAX_MSG", 100)
msg_list = []

app = FastAPI(docs_url=None, redoc_url=None)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    global max_msg
    try:
        max_msg = int(max_msg)
    except Exception as e:
        logger.error(e)
        max_msg = 20
        logger.info('Use the default value of max_msg = 20')


def log_request(message: str, method: str):
    try:
        global msg_list
        msg_list.append(f"{datetime.now()} - {method} - {message}")
        msg_list = msg_list[-max_msg:]
    except Exception as e:
        logger.error(e)


@app.get("/", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
        <head><title>FastAPI HTML Example</title></head>
        <body>
            <h1>Hello, this is a static HTML page in FastAPI!</h1>
        </body>
    </html>
    """


@app.api_route("/send", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def webhook(request: Request):
    try:
        method = request.method
        body = await request.body()
        message = body.decode('utf-8')
        log_request(message, method)
        return {"message": "Message received and logged"}
    except Exception as e:
        logger.error(e)
        return {"Error": str(e)}
