from time import sleep
from bhaptics import better_haptic_player as player
import keyboard
import asyncio

player.initialize()

# tact file can be exported from bhaptics designer
player.register("Electric1_back", "bhapticsPatterns/Electric1_back.tact")
player.register("Circle", "bhapticsPatterns/Circle.tact")
player.register("CenterX", "bhapticsPatterns/CenterX.tact")
player.register("Impact1","bhapticsPatterns/Impact1.tact")
player.register("Impact1","bhapticsPatterns/Impact1.tact")
player.register("Impact1_weak","bhapticsPatterns/Impact1_weak.tact")
player.register("Impact2","bhapticsPatterns/Impact2.tact")
player.register("Impact2_weak","bhapticsPatterns/Impact2_weak.tact")
player.register("Impact3","bhapticsPatterns/Impact3.tact")
player.register("Impact3_weak","bhapticsPatterns/Impact3_weak.tact")


async def impact(offsetAngleX=0,offsetY=0):
    player.submit_registered_with_option("Impact3", "alt",
                                         scale_option={"intensity": 1, "duration": 1},
                                         rotation_option={"offsetAngleX": offsetAngleX, "offsetY": offsetY})

    # direction means how long the pattern takes
    # offset AngleX will rotate pattern around the person. 180 moves the pattern from front to back
    # offsetY moves Pattern up toward head. Offset 0.25 moves up by one dot.
    # intesity is range between 0 and 1. Intensity percentage.

async def main():
    t = asyncio.create_task(impact())
    await t

if __name__ == "__main__":
    asyncio.run(main())