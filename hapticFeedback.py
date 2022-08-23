from time import sleep
from bhaptics import better_haptic_player as player
import keyboard
import asyncio
import random

player.initialize()

# tact file can be exported from bhaptics designer
player.register("Electric_front_and_back", "bhapticsPatterns/Rumble2.tact")
player.register("Circle", "bhapticsPatterns/Circle.tact")
player.register("CenterX", "bhapticsPatterns/CenterX.tact")
player.register("Heatbeat2", "bhapticsPatterns/Heartbeat2.tact")
player.register("Heatbeat3", "bhapticsPatterns/Heartbeat3.tact")


impact_patterns = ["Impact1", "Impact2", "Impact3"]


kinda_fire = ["Impact6", "Impact7"]

player.register("Piercing1","bhapticsPatterns/Piercing1.tact")


for p in impact_patterns:
    player.register(p, "bhapticsPatterns/"+p+".tact")


async def impact_unshielded(rotation=0,offsetY=0):
    if isdowned:
        return
    pattern = random.choice(impact_patterns)
    player.submit_registered_with_option(pattern, "alt",
                                         scale_option={"intensity": 1, "duration": 0.5},
                                         rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})

    # direction means how long the pattern takes
    # offset AngleX will rotate pattern around the person. 180 moves the pattern from front to back
    # offsetY moves Pattern up toward head. Offset 0.25 moves up by one dot.
    # intesity is range between 0 and 1. Intensity percentage.

async def impact_shielded(rotation=0,offsetY=0):
    if isdowned:
        return
    pattern = random.choice(impact_patterns)
    player.submit_registered_with_option(pattern, "alt",
                                         scale_option={"intensity": random.uniform(0.15,0.3), "duration": 0.5},
                                         rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})

async def eletrifiiieeeeddddd_iiiiiiiiieeeeeeeeddd(rotation=0,offsetY=0):
    player.submit_registered_with_option("Electric_front_and_back", "alt",
                                         scale_option={"intensity": 0.5, "duration": 1},
                                         rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})

isdowned = False

async def downed():
    global isdowned
    isdowned = True
    while(isdowned):

        player.submit_registered("Heatbeat2")
        await asyncio.sleep(1)

async def stopDowned():
    global isdowned
    isdowned = False