# pain_simulation_haptics

Second half of https://github.com/CodeIsJustLikeMagic/pain_simulation_payday_mod
A Payday 2 mod that customizes damage Feedback.

pain_simulation_haptics is a server that gets called by the Mod to perform haptic feedback.
Calls bHaptics Player and connects to an Arduino via USB serial connection. The Arduino performs thermal Feedback with a Peltier device.
Arduino Code is located in /firmware_thermal.

pain_simulation_haptics also recieves game data and compiles them into one file for evaluation.

----------------
Run: 

Before starting pain_simulation_haptics: turn bHaptics Player on, and connect hapitc Vest. Also connect Arduino and start the power supply for the Peltier devices.  
Then start pain_simulation_haptics before entering Payday Heist. (The Server needs to recieve the "load_profile" call to know which feedback profile should be loaded and used.)

---------------
Evaluation links:

evaluation has already been performed. Thank you to everyone who participated!

--------------

Setup: 
- Install bHaptics player https://www.bhaptics.com/support/download

Kalibration/Debugging calls: 
- http://localhost:8001/debug/bhaptic
- http://localhost:8001/debug/bhapticintensity/0.5
- http://localhost:8001/debug/coldstart
- http://localhost:8001/debug/coldleft
- http://localhost:8001/debug/coldright
- http://localhost:8001/debug/thermalintensity/255
- http://localhost:8001/debug/resetintensities

Calls for haptic feedback:
- http://localhost:8001/event/load_profile/Profile-Visual+Weste+Thermal+Sound.json
- http://localhost:8001/event/damage_taken_unshielded/0
- http://localhost:8001/event/damage_taken_shielded/0
- http://localhost:8001/event/downed
- http://localhost:8001/event/arrested
- http://localhost:8001/event/custody
- http://localhost:8001/event/revived
- http://localhost:8001/event/tased
- http://localhost:8001/event/tasestoped
- http://localhost:8001/event/stop_feedback

Calls for evaluation (there are more): 
- http://localhost:8001/evaluate/loadprofile/Profile2?playertag=example
- http://localhost:8001/evaluate/saveevalfile
