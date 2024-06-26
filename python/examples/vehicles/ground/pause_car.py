import time

from autonomysim.clients import CarClient, CarControls
from autonomysim.utils import SetupPath


def main():
    SetupPath()

    # connect to the AutonomySim simulator
    client = CarClient()
    client.confirmConnection()
    client.enableApiControl(True)

    car_controls = CarControls()

    for i in range(1, 6):
        print("Starting command")
        car_controls.throttle = 0.5
        car_controls.steering = 1
        client.setCarControls(car_controls)
        time.sleep(5)  # run
        print("Pausing after 5sec")
        client.simPause(True)
        time.sleep(5)  # paused
        print("Restarting command to run for 10sec")
        client.simContinueForTime(10)
        time.sleep(20)
        print("Finishing rest of the command")
        client.simPause(False)
        time.sleep(10)
        print("Finished cycle")


if __name__ == "__main__":
    main()
