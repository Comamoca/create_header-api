from fastapi import FastAPI
from src import generate
from src import converter as conv

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/header")
async def hello(
    twitter_id: str,
    icon_str: str = "./icon.txt",
    word: str = "",
    youtube_name: str = "",
    insta_name: str = "",
    fbook_name: str = "",
):

    with open(icon_str, "r") as f:
        icon_str = f.read()

    img = generate.create(
        icon_str, twitter_id, word, youtube_name, insta_name, fbook_name
    )

    ret = {"header": img}
    return ret
