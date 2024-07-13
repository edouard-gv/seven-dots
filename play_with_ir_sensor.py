from gpiozero import MotionSensor
from datetime import datetime

# datetime object containing current date and time
print(datetime.now())
pir = MotionSensor(4)






while True:
    pir.wait_for_motion()
    print(datetime.now())
    print("Motion detected!")
    pir.wait_for_inactive()
    print(datetime.now())
    print("Nobody's there detected!")