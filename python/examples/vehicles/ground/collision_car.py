import time
import pprint

from autonomysim.clients import CarClient, CarControls
from autonomysim.utils import SetupPath


def main():
    SetupPath()

    # connect to the AutonomySim simulator
    client = CarClient()
    client.confirmConnection()
    client.enableApiControl(True)
    car_controls = CarControls()

    client.reset()

    client.simPrintLogMessage("Hello", "345", 2)

    # go forward
    car_controls.throttle = 0.5
    car_controls.steering = 0
    client.setCarControls(car_controls)

    while True:
        # get state of the car
        car_state = client.getCarState()
        print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

        collision_info = client.simGetCollisionInfo()

        if collision_info.has_collided:
            print(
                "Collision at pos %s, normal %s, impact pt %s, penetration %f, name %s, obj id %d"
                % (
                    pprint.pformat(collision_info.position),
                    pprint.pformat(collision_info.normal),
                    pprint.pformat(collision_info.impact_point),
                    collision_info.penetration_depth,
                    collision_info.object_name,
                    collision_info.object_id,
                )
            )
            break

        time.sleep(0.1)

    client.enableApiControl(False)


if __name__ == "__main__":
    main()
