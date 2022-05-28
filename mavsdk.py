#!/usr/bin/env python3

import asyncio
import time

# Import MAVSDK
from mavsdk import System

# Async Python - run the main code body
# Note that since most MAVSDK actions run async,
# they need to be run using the await keyword
async def run():
  drone = System()
  await drone.connect(system_address="udp://:14540")

  print("Waiting for drone...")
  async for state in drone.core.connection_state():
    # This will basically run every time a drone connects
    if state.is_connected:
      print(f"Drone discovered with UUID: {state.uuid}")
      break


  print("-- Arming")
  await drone.action.arm()

  print("-- Taking off")
  # https://mavsdk.mavlink.io/develop/en/api_reference/classmavsdk_1_1_action.html#classmavsdk_1_1_action_1ace2188fe367b3bb10b17b89c88d1f952 - may help to read
  drone.action.set_takeoff_altitude(100)
  print (await drone.action.get_takeoff_altitude())
  await drone.action.takeoff()
  await asyncio.sleep(30)
  
  print("-- Landing")
  await drone.action.land()



loop = asyncio.get_event_loop()
loop.run_until_complete(run())