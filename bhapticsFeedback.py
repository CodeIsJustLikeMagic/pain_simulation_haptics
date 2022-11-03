from bhaptics import better_haptic_player as player
import asyncio
import random
import json
from collections import namedtuple

print("bhapticFeedback initialize")

player.initialize()

# tact file can be exported from bhaptics designer
# register Patters with bHaptics Player so they can be used later
player.register("Electric_front_and_back", "bhapticsPatterns/Rumble2.tact")
player.register("Circle", "bhapticsPatterns/Circle.tact")
player.register("CenterX", "bhapticsPatterns/CenterX.tact")
player.register("Heartbeat2", "bhapticsPatterns/Heartbeat2.tact")
player.register("Heartbeat3", "bhapticsPatterns/Heartbeat3.tact")

impact_patterns = ["Impact1", "Impact2", "Impact3"]

kinda_fire = ["Impact6", "Impact7"]

player.register("Piercing1", "bhapticsPatterns/Piercing1.tact")

HapticEffect = namedtuple("HapticEffect",
                          "patterns lowerbound upperbound duration extra")  # extra is rotation(true false) for effects that are played one and sleep for looped effect

shieldedEffect: HapticEffect = None
unshieldedEffect: HapticEffect = None
tasedEffect: HapticEffect = None
downedEffect: HapticEffect = None


# is run when game is loaded
async def loadProfile(path):
    print(f"loaded profile from {path}")
    global shieldedEffect
    global unshieldedEffect
    global tasedEffect
    global downedEffect

    profileFile = open(path)
    profile = json.load(profileFile)
    profileFile.close()

    shieldedEffect = _createHapticEffect(profile["shielded"], "rotation")
    unshieldedEffect = _createHapticEffect(profile["unshielded"], "rotation")
    tasedEffect = _createHapticEffect(profile["tased"], "sleep")
    downedEffect = _createHapticEffect(profile["downed"], "sleep")



def _createHapticEffect(haptic_settings, extraProperty="rotation"):
    if "haptic" in haptic_settings:
        haptic_settings = haptic_settings["haptic"]
        effect = HapticEffect(haptic_settings["patterns"], haptic_settings["lowerbound"], haptic_settings["upperbound"],
                              haptic_settings["duration"], haptic_settings[extraProperty])
        print("bhapticFeedback hapic effect created")
        return effect
    else:
        print("bhapticFeedback no haptic effect found in profile")
        return None # make sure to remove effect if none are wanted. Should make switching from haptic profile to non haptic profile work


for p in impact_patterns:
    player.register(p, "bhapticsPatterns/" + p + ".tact")


async def shielded_hit(rotation=0, offsetY=0):
    print("bhapticFeedback impact_shielded")
    if isdowned or iselectrefied or shieldedEffect is None:
        return
    pattern = random.choice(shieldedEffect.patterns)
    intensity = random.uniform(shieldedEffect.lowerbound, shieldedEffect.upperbound)
    if shieldedEffect.extra == "false":
        rotation = 0
    player.submit_registered_with_option(pattern, "alt",
                                         scale_option={"intensity": intensity, "duration": shieldedEffect.duration},
                                         rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})

async def unshielded_hit(rotation=0, offsetY=0):
    print("bhapticFeedback impact_unshielded")
    if isdowned or iselectrefied or unshieldedEffect is None:
        return
    pattern = random.choice(unshieldedEffect.patterns)
    intensity = random.uniform(unshieldedEffect.lowerbound, unshieldedEffect.upperbound)
    if unshieldedEffect.extra == "false":
        rotation = 0
    player.submit_registered_with_option(pattern, "alt",
                                         scale_option={"intensity": intensity, "duration": unshieldedEffect.duration},
                                         rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})

    # direction means how long the pattern takes
    # offset AngleX will rotate pattern around the person. 180 moves the pattern from front to back
    # offsetY moves Pattern up toward head. Offset 0.25 moves up by one dot.
    # intesity is range between 0 and 1. Intensity percentage.


# looped Effects
iselectrefied = False


async def eletrifiiieeeeddddd_iiiiiiiiieeeeeeeeddd(rotation=0, offsetY=0):
    print("bhapticFeedback tased")
    if isdowned or tasedEffect is None:
        return
    global iselectrefied
    iselectrefied = True
    while iselectrefied:
        pattern = random.choice(tasedEffect.patterns)
        intensity = random.uniform(tasedEffect.lowerbound, tasedEffect.upperbound)
        player.submit_registered_with_option(pattern, "alt",
                                             scale_option={"intensity": intensity, "duration": tasedEffect.duration},
                                             rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})
        await asyncio.sleep(tasedEffect.extra)


async def stop_tased():
    print("bhapticFeedback tase stoped")
    global iselectrefied
    iselectrefied = False
    player.submit_registered_with_option("Circle","alt",
                                         scale_option={"intensity": 0, "duration": 0.01},
                                         rotation_option={"offsetAngleX": 0, "offsetY": 0})

isdowned = False


async def downed(rotation=0, offsetY=0):
    print("bhapticFeedback downed")
    if iselectrefied:
        await stop_tased()
    if downedEffect is None:
        return
    global isdowned
    isdowned = True
    while isdowned:

        pattern = random.choice(downedEffect.patterns)
        intensity = random.uniform(downedEffect.lowerbound, downedEffect.upperbound)
        print(f"downed {pattern} intensity {intensity} duration {downedEffect.duration} rotation {rotation}")
        player.submit_registered_with_option(pattern, "alt",
                                             scale_option={"intensity": intensity, "duration": downedEffect.duration},
                                             rotation_option={"offsetAngleX": rotation, "offsetY": offsetY})
        await asyncio.sleep(downedEffect.extra)


async def stop_downed():
    print("bhapticFeedback stop downed")
    global isdowned
    isdowned = False
