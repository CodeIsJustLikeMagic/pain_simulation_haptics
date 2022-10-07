import asyncio
import os.path
from typing import Optional
import datetime
from fastapi import FastAPI
import pandas as pd
import hapticFeedback

app = FastAPI()

eval_df = pd.DataFrame(columns=['Player', 'Profile', 'Time', 'Event'])

player = "unknown"
profile = "unknown"

level_start = datetime.datetime.now()

@app.get("/")
def read_root():
    return {"Hello": "World"}


#region haptic events
@app.get("/event/load_profile/{profile}")
async def read_item(profile:str):
    path = os.path.join(r"C:/Program Files (x86)/Steam/steamapps/common/PAYDAY 2/mods/pain_simulation_payday", profile)
    t = asyncio.create_task(hapticFeedback.loadProfile(path))
    return {"received"}

@app.get("/event/stop_feedback")
async def read_item():
    t = asyncio.create_task(hapticFeedback.stop_downed())
    t = asyncio.create_task(hapticFeedback.stop_tased())
    return {"recieved"}

#http://localhost:8001/event/damage_taken_shielded
@app.get("/event/damage_taken_shielded/{rotation}")
async def read_item(rotation:float):
    t = asyncio.create_task(hapticFeedback.impact_shielded(rotation))
    return {"received"}

@app.get("/event/damage_taken_unshielded/{rotation}")
async def read_item(rotation:float):
    t = asyncio.create_task(hapticFeedback.impact_unshielded(rotation))
    return {"received"}

@app.get("/event/downed")
async def read_item():
    t = asyncio.create_task(hapticFeedback.downed())
    return {"received"}

@app.get("/event/revived")
async def read_item():
    # no longer downed
    t = asyncio.create_task(hapticFeedback.stop_downed())
    return {"received"}

@app.get("/event/arrested")
async def read_item():
    t = asyncio.create_task(hapticFeedback.stop_downed())
    return {"received"}

@app.get("/event/custody")
async def read_item():
    t = asyncio.create_task(hapticFeedback.stop_downed())
    return {"received"}

@app.get("/event/tased")
async def read_item():
    t = asyncio.create_task(hapticFeedback.eletrifiiieeeeddddd_iiiiiiiiieeeeeeeeddd())
    return {"received"}

@app.get("/event/tasestoped")
async def read_item():
    t = asyncio.create_task(hapticFeedback.stop_tased())
    return {"received"}

#endregion

#region evaluation
def documentAction(action):
    eval_df.loc[len(eval_df.index)] = [player, profile, datetime.datetime.now(), action]

#http://localhost:8001/evaluate/levelload/profile1?playertag=example
@app.get("/evaluate/loadprofile/{profilfile}")
async def read_item(profilfile: str, playertag:str):
    global eval_df
    global level_start
    global player
    global profile
    player = playertag
    profile = os.path.splitext(profilfile)[0]
    eval_df = pd.DataFrame(columns=['Player', 'Profile', 'Time', 'Event'])
    level_start = datetime.datetime.now()
    print(f"ready to write Evaluation file into Stats/"+player+"_"+profile+"_"+str(level_start.strftime("%y_%m_%d__%H_%M"))+".csv")
    return {"received"}

@app.get("/evaluate/saveevalfile/{session_accuracy}")
async def read_item(session_accuracy:str, session_total_downed:str, session_total_kills: str, session_total_head_shots: str, session_total_specials_kills: str, session_civilian_kills:str):

    documentAction("Session_Accuracy "+str(session_accuracy))
    #documentAction("Session_time_played "+str(session_time_played))
    documentAction("Session_total_downed " +str(session_total_downed))
    documentAction("Session_total_kills "+str(session_total_kills))
    documentAction("Session_total_head_shots "+str(session_total_head_shots))
    documentAction("Session_total_specials_kills "+str(session_total_specials_kills))
    documentAction("Session_civilians_killed "+str(session_civilian_kills))

    print(f"saving eval dataframe with session stats to Stats/"+player+"_"+profile+"_"+str(level_start.strftime("%y_%m_%d__%H_%M"))+".csv")
    eval_df.to_csv("Stats/"+player+"_"+profile+"_"+str(level_start.strftime("%y_%m_%d__%H_%M"))+".csv")
    return {"received"}

@app.get("/evaluate/saveevalfile")
async def read_item():

    print(f"saving eval dataframe Stats/"+player+"_"+profile+"_"+str(level_start.strftime("%y_%m_%d__%H_%M"))+".csv")
    eval_df.to_csv("Stats/"+player+"_"+profile+"_"+str(level_start.strftime("%y_%m_%d__%H_%M"))+".csv")
    return {"received"}

@app.get("/evaluate/killshot")
async def read_item():
    documentAction("killed an enemy")
    return {"received"}

@app.get("/evaluate/unshielded")
async def read_item():
    documentAction("unshielded hit")
    return {"received"}

@app.get("/evaluate/tased")
async def read_item():
    documentAction("tased")
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

@app.get("/evaluate/weapon_fired/{hit_count}")
async def read_item(hit_count: int):
    documentAction(f"weapon_fired {hit_count}")
    # hit count is 0 if player missed.
    # accuracy can be over 100 percent if player hits more that one person per shot
    return {"received"}

@app.get("/evaluate/enemy_headshot")
async def read_item():
    documentAction("enemy_headshot")
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

#endregion
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)