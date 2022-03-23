import asyncio
from typing import Optional
import datetime
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


async def takes_frever():
    await asyncio.sleep(200)

@app.get("/event/level_load")
async def read_item():#, q: Optional[str] = None
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} level_load")
    return {"received"}

@app.get("/event/shield/{value}")
async def read_item(value: int):#, q: Optional[str] = None
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} set shield with value {value}")
    return {"received"}

@app.get("/event/health/{value}")
async def read_item(value: int):
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} set health with value {value}")
    return {"received"}

@app.get("/event/damage_taken")
async def read_item():
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} damage_taken")
    return {"received"}

@app.get("/event/downed")
async def read_item():
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} downed")
    return {"received"}

@app.get("/event/arrested")
async def read_item():
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} arrested")
    return {"received"}

@app.get("/event/custody")
async def read_item():
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} custody")
    return {"received"}

@app.get("/evaluate/killshot")
async def read_item():
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} enemy killshot")
    return {"received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)