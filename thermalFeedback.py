import datetime
import time
import serial
import asyncio
import json

#region manage serial connection

ser: serial.Serial = None
def connect_to_arduino():
    global ser
    if ser is not None:
        ser.close()
    ser = None
    try:
        print("thermalFeedback initialize")
        ser = serial.Serial('COM3', 115200)
        print("thermalFeedback successfully connected to Arduino")
    except serial.serialutil.SerialException:
        print("thermalFeedback could not find Arduino. Make sure it is connected to PC via USB")

connect_to_arduino()
cold_duration = 3
pwm = 255 # pwm of peltier element. Range between 0 and 255. 255 is as much cooling/heating as the given voltage allows.
# pwm stands for pulse weiten modulation. The peltier element will be switched on and off quickly (as if dimming an LED)

async def startCold(peltierElements=None):
    if peltierElements is None:
        peltierElements = [0, 1]
    print(f"thermalFeedback start cold {datetime.datetime.now()}")
    if ser is not None:
        try:
            for peltier in peltierElements:
                ser.write(str.encode(f"{peltier} {pwm}\r\n")) # looks like this: 0 255
            ser.flush()
            print("thermal wrote to serial connection")
        except serial.serialutil.SerialTimeoutException:#if arduino is disconnected
            print("thermal arduino unexpectedly disconnected")
            connect_to_arduino() # attempt to reconnect. If it doesn't work don't do thermal feedback

    await asyncio.sleep(cold_duration)
    t = asyncio.create_task(stopCold())

async def stopCold():
    print("thermalFeedback stop cold")
    if ser is not None:
        try:
            ser.write(b'0 10\r\n') # let peltier element run at low power. This way the "cool side" doesn't start to feel warm as the peltier element is dissapating heat
            ser.write(b'1 10\r\n')
            ser.flush()
        except serial.serialutil.SerialTimeoutException:  # if arduino is disconnected after serial connection initally worked
            print("thermal arduino unexpectedly disconnected")
            connect_to_arduino()  # attempt to reconnect. If it doesn't work don't do thermal feedback

def cleanup():
    if ser is not None:
        ser.write(b'0 0\r\n')# peltier 0, pwm 0
        ser.write(b'1 0\r\n')# peltier 1, pwm 0
        ser.flush()
        ser.close()

import atexit
atexit.register(cleanup)

#endregion

# region gameIntegration

hits_to_trigger_cold = 3
time_span_to_trigger_cold = 3

last_hits = [] # save last three hits in queue

# allow peltier element time to dissapate heat, otherwise the element feels noticably warm even on the cool side.
cold_cooldown = 10
last_cold_trigger = 0

async def shielded_hit():
    # want to count how many hits we get. If we get lets say 3 hits in a span of 3 seconds start cold
    global last_cold_trigger
    last_hits.append(time.time()) # append newest hit and throw oldes hit out if we now have to many in the queue
    if len(last_hits) > hits_to_trigger_cold:
        last_hits.pop(0)

    print(last_hits)
    if len(last_hits) == hits_to_trigger_cold: # check if we have three hits
        if last_hits[-1] - last_cold_trigger > cold_cooldown: # check cooldown time between cold activations
            if last_hits[-1] - last_hits[0] < time_span_to_trigger_cold: #are hits in small enough time window?
                t = asyncio.create_task(startCold())
                last_cold_trigger = last_hits[-1]
                last_hits.clear()


async def unshielded_hit():
    t = asyncio.create_task(shielded_hit())

async def downed():
    global last_cold_trigger
    t = asyncio.create_task(startCold())
    last_cold_trigger = time.time()
    last_hits.clear()

async def stop_downed():
    t = asyncio.create_task(stopCold())


async def eletrifiiieeeeddddd_iiiiiiiiieeeeeeeeddd():
    global last_cold_trigger
    t = asyncio.create_task(startCold())
    last_cold_trigger = time.time()
    last_hits.clear()


async def stop_tased():
    t = asyncio.create_task(stopCold())

async def loadProfile(path): # need to load if we want thermal feedback to be active
    try:
        profileFile = open(path)
        profile = json.load(profileFile)
        profileFile.close()
        if "thermalfeedback" in profile and profile["thermalfeedback"] == "true":
            print("thermalFeedback enabled via feedback profile")
            connect_to_arduino()  # new connection to Arduino automatically stops cold.
        else:
            cleanup() # if peltier was active before, deactivate and close connection
            print("thermalFeedback disabled via feedback profile")
    except FileNotFoundError:
        print(f"Error !!!! thermal feedback cound not find profile {path}")
        cleanup()  # if peltier was active before, deactivate and close connection
        print("thermalFeedback disabled")
#endregion
async def modifyIntensity(pwm_): # set pwm in kalibration step through /debug/thermalintensity/{pwm}
    global pwm
    pwm = pwm_