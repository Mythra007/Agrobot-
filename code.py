Python 3.12.7 (tags/v3.12.7:0b05ead, Oct  1 2024, 03:06:41) [MSC v.1941 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import pybullet as p
... import pybullet_data
... import time
... import math
... 
... # Setup
... physicsClient = p.connect(p.GUI)
... p.setAdditionalSearchPath(pybullet_data.getDataPath())
... p.setGravity(0, 0, -9.8)
... 
... plane = p.loadURDF("plane.urdf")
... robot = p.loadURDF("agro_bot.urdf", basePosition=[0, 0, 0.1])
... 
... L = 10  # Field length
... B = 10  # Field breadth
... GRID_SIZE = L / 10  # 10x10 grid
... WHEEL_VEL = 10.0
... SLEEP_STEP = 1.0 / 240.0
... 
... # Wheel joint indices
... left_front = 0
... right_front = 1
... left_back = 2
... right_back = 3
... 
... def get_position():
...     pos, _ = p.getBasePositionAndOrientation(robot)
...     return pos[0], pos[1]
... 
... def set_wheel_velocity(l_speed, r_speed):
...     p.setJointMotorControl2(robot, left_front, p.VELOCITY_CONTROL, targetVelocity=l_speed, force=100)
...     p.setJointMotorControl2(robot, left_back, p.VELOCITY_CONTROL, targetVelocity=l_speed, force=100)
...     p.setJointMotorControl2(robot, right_front, p.VELOCITY_CONTROL, targetVelocity=r_speed, force=100)
...     p.setJointMotorControl2(robot, right_back, p.VELOCITY_CONTROL, targetVelocity=r_speed, force=100)

def stop_robot():
    set_wheel_velocity(0, 0)
    print("stopped")
    time.sleep(0.5)


def move_one_grid():
    start_x, start_y = get_position()
    set_wheel_velocity(WHEEL_VEL, WHEEL_VEL)
    while True:
        p.stepSimulation()
        time.sleep(SLEEP_STEP)
        x, y = get_position()
        dx = x - start_x
        dy = y - start_y
        dist = math.sqrt(dx**2 + dy**2)
        if dist >= GRID_SIZE:
            break
        print(f"dist: {dist:.2f}")

    stop_robot()

def turn180():
    print("turning")
    row = int(get_position()[1] * 10 / B)
    if row % 2 == 0:
        set_wheel_velocity(WHEEL_VEL, -WHEEL_VEL)
    else:
        set_wheel_velocity(-WHEEL_VEL, WHEEL_VEL)
    t = 0
    duration = 62.8/WHEEL_VEL  # Adjust as needed for 180 degrees
    while t < duration:
        p.stepSimulation()
        time.sleep(SLEEP_STEP)
        t += SLEEP_STEP
    stop_robot()

def gridNumber(x, y):
    x_no = int(x * 10 / L)  # column index (0–9)
    y_no = int(y * 10 / B)  # row index (0–9)
    grid_no = y_no * 10 + x_no + 1  # +1 for 1-based indexing
    return grid_no

# Main loop
for step in range(100):
    x, y = get_position()
    if grid_number(x, y) % 10 == 0:
        turn180()
        move_one_grid()
    else:
