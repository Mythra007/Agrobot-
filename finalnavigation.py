import pybullet as p
import pybullet_data
import time
import math

# Setup
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

plane = p.loadURDF("plane.urdf")
robot = p.loadURDF("agro_bot.urdf", basePosition=[0, 0, 0.1])

L = 10  # Field length
B = 10  # Field breadth
GRID_SIZE = L / 10  # 10x10 grid
WHEEL_VEL = 10.0
SLEEP_STEP = 1.0 / 240.0

# Wheel joint indices
left_front = 0
right_front = 1
left_back = 2
right_back = 3

def get_position():
    pos, _ = p.getBasePositionAndOrientation(robot)
    return pos[0], pos[1]

def set_wheel_velocity(l_speed, r_speed):
    p.setJointMotorControl2(robot, left_front, p.VELOCITY_CONTROL, targetVelocity=l_speed, force=100)
    p.setJointMotorControl2(robot, left_back, p.VELOCITY_CONTROL, targetVelocity=l_speed, force=100)
    p.setJointMotorControl2(robot, right_front, p.VELOCITY_CONTROL, targetVelocity=r_speed, force=100)
    p.setJointMotorControl2(robot, right_back, p.VELOCITY_CONTROL, targetVelocity=r_speed, force=100)

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
 
 def turn90(row):
    """
    Turn 90 degrees: left for even rows, right for odd rows
    """
    import math

    # Left turn for even rows, right turn for odd rows
    direction = 1 if row % 2 == 0 else -1

    _, orientation = p.getBasePositionAndOrientation(robot)
    _, _, start_yaw = p.getEulerFromQuaternion(orientation)

    # Normalize yaw to range [-π, π]
    start_yaw = (start_yaw + math.pi) % (2 * math.pi) - math.pi

    # Compute target yaw after 90-degree turn
    target_yaw = start_yaw + direction * (math.pi / 2)
    target_yaw = (target_yaw + math.pi) % (2 * math.pi) - math.pi

    # Start turning
    set_wheel_velocity(WHEEL_VEL * direction, -WHEEL_VEL * direction)

    while True:
        p.stepSimulation()
        time.sleep(SLEEP_STEP)
        _, orientation = p.getBasePositionAndOrientation(robot)
        _, _, current_yaw = p.getEulerFromQuaternion(orientation)
        current_yaw = (current_yaw + math.pi) % (2 * math.pi) - math.pi

        # Calculate shortest angular distance to target
        angle_diff = (target_yaw - current_yaw + math.pi) % (2 * math.pi) - math.pi

        if abs(angle_diff) < 0.05:  # within ~2.8°
            break

    stop_robot()