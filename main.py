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

@app.get("/event/shield/{value}")
async def read_item(value: int):#, q: Optional[str] = None
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} set shield with value {value}")
    return {"success"}

@app.get("/event/health/{value}")
async def read_item(value: int):#, q: Optional[str] = None
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} set health with value {value}")
    return {"success"}

@app.get("/event/damage_taken")
async def read_item():#, q: Optional[str] = None
    t = asyncio.create_task(takes_frever())
    print(f"{datetime.datetime.now()} damage_taken")
    return {"success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)