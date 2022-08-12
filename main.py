import asyncio
from typing import Optional
import datetime
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

eval_df = pd.DataFrame(columns=['Player', 'Profile', 'Time', 'Event'])

player = "test"
profile = "profile1"

level_start = datetime.datetime.now()

@app.get("/")
def read_root():
    return {"Hello": "World"}


async def takes_frever():
    await asyncio.sleep(200)

#http://localhost:8001/event/level_load/
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



def documentAction(action):
    eval_df.loc[len(eval_df.index)] = [player, profile, datetime.datetime.now(), action]

@app.get("/evaluate/levelload")
async def read_item():
    global eval_df
    global level_start
    eval_df = pd.DataFrame(columns=['Player', 'Profile', 'Time', 'Event'])
    level_start = datetime.datetime.now()
    documentAction("LevelLoad")
    documentAction("killed an enemy")
    return {"received"}

@app.get("/evaluate/levelquit")
async def read_item():

    documentAction("LevelQuit")
    eval_df.to_csv("Stats/"+player+"_"+profile+"_"+str(level_start.strftime("%y_%m_%d__%H_%M"))+".csv")

    documentAction("killed an enemy")
    return {"received"}

@app.get("/evaluate/killshot")
async def read_item():
    documentAction("killed an enemy")
    return {"received"}

@app.get("/evaluate/unshielded")
async def read_item():
    documentAction("unshielded hit")
    return {"received"}

@app.get("/evaluate/shielded")
async def read_item():
    documentAction("shielded hit")
    return {"received"}

@app.get("/evaluate/regeneratearmor")
async def read_item():
    documentAction("auto regenerate armor")
    return {"received"}

@app.get("/evaluate/downed")
async def read_item():
    documentAction("downed")
    return {"received"}

@app.get("/evaluate/revived")
async def read_item():
    documentAction("revived by ally")
    return {"received"}

@app.get("/evaluate/replenish")
async def read_item():
    documentAction("auto replenish health")
    return {"received"}

@app.get("/evaluate/doctor_bag_used")
async def read_item():
    documentAction("doctor_bag")
    return {"received"}

@app.get("/evaluate/enemy_hit")
async def read_item():
    documentAction("enemy_hit")
    return {"received"}

@app.get("/evaluate/enemy_headshot")
async def read_item():
    documentAction("enemy_headshot")
    return {"received"}

@app.get("/evaluate/enemy_crit")
async def read_item():
    documentAction("enemy_crit")
    return {"received"}


#http://localhost:8001/evaluate/sethp/30?armor=0
@app.get("/evaluate/sethp/{hp}")
async def read_item(hp: int, armor:int):
    documentAction("hp "+str(hp))
    documentAction("armor " + str(armor))
    return {"received"}

@app.get("/evaluate/complete_objective/{objective}")
async def read_item(objective: str):
    documentAction("complete_objective "+str(objective))
    return {"received"}

@app.get("/evaluate/activate_objective/{objective}")
async def read_item(objective: str):
    documentAction("activate_objective "+str(objective))
    return {"received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)