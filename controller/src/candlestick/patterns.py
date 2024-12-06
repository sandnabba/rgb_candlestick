import random
import copy
import logging
from time import sleep
from random import randint

logger = logging.getLogger(__name__)

directions = ["right", "up", "down", "left"]

# TODO: Combine this into a dictionary instead:
red = [250, 0, 0]
orange = [250, 127, 0]
yellow = [250, 250, 0]
green = [0, 250, 0]
blue = [0, 0, 250]
cyan = [139, 0, 250]
white = [250, 250, 250]
black = [0, 0, 0]
colors = [red, orange, yellow, green, cyan, blue, white]

old_random = None

########## Support functions #################
def get_random_color():
    global old_random
    new_random = randint(0,6)
    while new_random is old_random:
        new_random = randint(0,6)
    old_random = new_random
    return colors[new_random]

def speed_sleep(delay, speed):
    # Normal is delay / 1
    if type(speed) is int:
        sleep_delay = delay / ((speed * 10) / 100)
    else:
        if speed.value >= 10:
            sleep_delay = delay / ((speed.value * (speed.value / 5 )) / 20 )
        else:
            sleep_delay = delay / ((speed.value * 10 ) / 100)
    logger.debug("Sleeping: %s", sleep_delay)
    sleep(sleep_delay)

def diff_set_array(controller, now, goal, direction=None, speed=10):
    """
    Gradually transitions an array of RGB values from `now` to `goal`.

    Args:
        controller: The object responsible for setting the RGB values.
        now (list): Current RGB values, a 7x3 array of integers.
        goal (list): Target RGB values, a 7x3 array of integers.
        direction: Optional parameter for the controller to specify direction.
        speed (int): Controls the transition speed (higher = faster).

    Returns:
        list: The final state of the RGB values (matches `goal`).
    """
    helper = copy.deepcopy(now)
    goal = copy.deepcopy(goal)
    steps = 50
    delay = 0.2 / speed.value

    for step in range(steps, 0, -1):
        for x in range(7):
            for i in range(3):
                a = float(helper[x][i])
                b = float(goal[x][i])
                difference = abs(a - b)

                if difference <= 2:
                    helper[x][i] = b
                else:
                    adjustment = difference / step
                    helper[x][i] = a + adjustment if a < b else a - adjustment

                helper[x][i] = int(helper[x][i])

        controller.set_full_array(helper, direction)
        sleep(delay)

    return helper


############### Patterns below here #################

def debug(direction=None):
    # while 1:
    #     #led = [red, orange, yellow, green, cyan, blue, white]
    #     led = [red, green, yellow, green, cyan, green, red]
    #     controller.set_full_array(led, direction)
    #     sleep(0.5)
    # sleep(5)
    led = [red, red, red, red, red, red, red]
    sleep(0.5)
    controller.set_full_array(led, direction)
    led = [green, green, green, green, green, green, green]
    sleep(0.5)
    controller.set_full_array(led, direction)
    led = [blue, blue, blue, blue, blue, blue, blue]
    sleep(0.5)
    controller.set_full_array(led, direction)


def cop(controller, rounds=4, direction=None, delay=0.5, color=None, speed=10):
    logger.info("Starting cop, %s rounds", rounds)
    counter = 0
    rounds_counter = 0
    flash = 3

    led1 = [
        red, blue, blue,
        blue,
        red, red, blue
    ]
    led2 = [
        blue, red, red,
        red,
        blue, blue, red
    ]

    while rounds_counter < rounds:
        while counter < flash:

            controller.set_full_array(led1, "right")
            speed_sleep(delay, speed)

            controller.set_full_array(led2, "right")
            speed_sleep(delay, speed)
            counter += 1

        counter = 0
        goal1 = copy.deepcopy(led1)
        goal1.append(goal1[0])
        goal1.remove(goal1[0])
        goal1.append(goal1[0])
        goal1.remove(goal1[0])
        goal2 = copy.deepcopy(led2)
        goal2.append(goal2[0])
        goal2.remove(goal2[0])
        goal2.append(goal2[0])
        goal2.remove(goal2[0])
        led1 = copy.deepcopy((goal1))
        led2 = copy.deepcopy((goal2))

        rounds_counter += 1

def bounce(controller, rounds=None, direction=None, delay=0.3, color=None, speed=10):
    if not direction:
        direction = random.choice(directions)
    if direction == "right" or direction == "left":
        led_count = 6
    else:
        led_count = 3
        delay = delay * 1.5
    if not rounds:
        if direction == "right" or direction == "left":
            rounds = 3
        else:
            rounds = 5
    logger.info("Studs, direction: %s, rounds: %s", direction, rounds)
    counter = 0
    while counter is not rounds:
        if not color:
            local_color = get_random_color()
        for x in range(led_count):
            controller.set_led(x, local_color, True, direction)
            # sleep(delay)
            speed_sleep(delay, speed)
            controller.set_led(x, black, False, direction)
        local_color = get_random_color()
        for x in range(led_count,-1,-1):
            controller.set_led(x, local_color, True, direction)
            # sleep(delay)
            speed_sleep(delay, speed)
            controller.set_led(x, black, False, direction)
        counter += 1
        logger.debug("%s", counter)

# TODO, not implemented.
# Bounce, but each LED will be of a random color
def bounce_random(controller, delay=0.5, speed=1):
    set_all()
    for x in range(6):
        controller.set_led(x, get_random_color())
        sleep(delay)
        controller.set_led(x, black, False)
    for x in range(6,-1,-1):
        controller.set_led(x, get_random_color())
        sleep(delay)
        controller.set_led(x, black, False)

def wave(controller, rounds=None, direction=None, delay=0.4, color=False, speed=10):
    if direction == None:
        direction = random.choice(directions)
        logger.info("Direction not set, going: %s", direction)
    else:
        logger.info("Direction set to: %s", direction)
    if direction == "right" or direction == "left":
        led_count = 7
    else:
        led_count = 4
    if not rounds:
        if direction == "right" or direction == "left":
            rounds = 4
        else:
            rounds = 6
    logger.info("Wave, direction: %s", direction)
    counter = 0
    while counter is not rounds:
        if not color:
            local_color = get_random_color()
        for x in range(led_count):
            controller.set_led(x, local_color, True, direction)
            speed_sleep(delay, speed)
        counter += 1
        logger.debug("%s", counter)

def fall(controller, rounds=None, direction=None, delay=0.15, color=None, speed=10):
    # if not direction:
    #     direction = random.choice(directions)
    if direction == "right" or direction == "left":
        led_count = 6
    else:
        led_count = 3
        delay = delay * 1.5
    if not rounds:
        if direction == "right" or direction == "left":
            rounds = 3
        else:
            rounds = 5
    logger.info("Fall, direction: %s, rounds: %s", direction, rounds)
    counter = 0
    first = True
    while counter is not rounds:
        if not color:
            local_color = get_random_color()
        for x in [4, 5, 6]:
            if x == 4:
                controller.set_led(3, black, False, direction)
            if x == 6:
                controller.set_led(3, local_color, False, direction)
            controller.set_led(x, local_color, True, direction)
            speed_sleep(delay, speed)
            controller.set_led(x, black, False, direction)

        for x in [2, 1, 0]:
            if x == 2:
                controller.set_led(3, black, False, direction)
            if x == 0:
                controller.set_led(3, local_color, False, direction)
            controller.set_led(x, local_color, True, direction)
            speed_sleep(delay, speed)
            controller.set_led(x, black, False, direction)
        counter += 1
        logger.debug("%s", counter)


def rb(controller, rounds=21, direction=None, delay=0.4, speed=10):
    """
    Displays a rainbow effect on LEDs, cycling through colors in the specified direction.

    Args:
        controller: The object responsible for setting the LED colors.
        rounds (int): Number of cycles to perform.
        direction: The direction of the rainbow animation. Randomly chosen if not provided.
        delay (float): Base delay between transitions.
        speed (int): Adjusts the delay (higher = faster transitions).
    """
    if direction is None:
        direction = random.choice(directions)
    logger.info("Rainbow effect, direction: %s", direction)

    # Initialize the rainbow colors
    led = [red, orange, yellow, green, cyan, blue, white]
    controller.set_full_array(led, direction)

    for counter in range(rounds):
        # Rotate the LED array by one position
        goal = led[1:] + [led[0]]

        # Transition to the new LED configuration
        led = diff_set_array(controller, led, goal, direction, speed)

        # Adjust speed-based delay
        speed_sleep(delay, speed)

        # Log progress
        logger.debug("Round: %d", counter + 1)


# Not used? Could probably be replaced by set_all directly
def blank():
    logger.info("Setting all black")
    # But read serial port:
    while True:
        set_all(black)
        sleep(60)

def set_color_from_api(controller, rgb_color):
    '''
    Special hacky function due to how it was implemented before, using a multiprocessing.Event()
    and a multiprocessing.Queue(). Today it could probably be implemented as a regular function.
    '''
    logger.debug("Set a static set of colors: %s", rgb_color)
    arr = [rgb_color[0], rgb_color[1], rgb_color[2]]
    controller.set_all(color=arr)
