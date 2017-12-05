from .rgb_support import *
import random


def cop(rounds=None, direction=None, delay=0.5, color=None, speed=10):
    rounds = 4
    print("Cop: ", rounds, " rounds")
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

            set_full_array(led1, "right")
            speed_sleep(delay, speed)

            set_full_array(led2, "right")
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

    print()

def bounce(rounds=None, direction=None, delay=0.3, color=None, speed=10):
    if not direction:
        direction = random.choice(directions)
    if direction is "right" or direction is "left":
        led_count = 6
    else:
        led_count = 3
        delay = delay * 1.5
    if not rounds:
        if direction is "right" or direction is "left":
            rounds = 3
        else:
            rounds = 5
    print("Studs, direction: ", direction, "", rounds, " rounds")
    counter = 0
    while counter is not rounds:
        if not color:
            local_color = get_random_color()
        for x in range(led_count):
            set_led(x, local_color, True, direction)
            # sleep(delay)
            speed_sleep(delay, speed)
            set_led(x, black, False, direction)
        local_color = get_random_color()
        for x in range(led_count,-1,-1):
            set_led(x, local_color, True, direction)
            # sleep(delay)
            speed_sleep(delay, speed)
            set_led(x, black, False, direction)
        counter += 1
        print(counter, "", end="", flush=True)
    print()

def random_studs(delay=0.5, speed=1):
    set_all()
    for x in range(6):
        set_led(x, get_random_color())
        sleep(delay)
        set_led(x, black, False)
    for x in range(6,-1,-1):
        set_led(x, get_random_color())
        sleep(delay)
        set_led(x, black, False)

def wave(rounds=None, direction=None, delay=0.4, color=False, speed=10):
    if direction == None:
        direction = random.choice(directions)
        print("Direction not set, going: ", direction)
    else:
        print("Direction set to: ", direction)
    if direction is "right" or direction is "left":
        led_count = 7
    else:
        led_count = 4
    if not rounds:
        if direction is "right" or direction is "left":
            rounds = 4
        else:
            rounds = 6
    print("Wave, direction: ", direction, "(", led_count, " leds), ", rounds, " rounds")
    counter = 0
    while counter is not rounds:
        if not color:
            local_color = get_random_color()
        for x in range(led_count):
            set_led(x, local_color, True, direction)
            speed_sleep(delay, speed)
        counter += 1
        print(counter, "", end="", flush=True)
    print()

def fall(rounds=None, direction=None, delay=0.15, color=None, speed=10):
    # if not direction:
    #     direction = random.choice(directions)
    if direction is "right" or direction is "left":
        led_count = 6
    else:
        led_count = 3
        delay = delay * 1.5
    if not rounds:
        if direction is "right" or direction is "left":
            rounds = 3
        else:
            rounds = 5
    print("Fall, direction: ", direction, "", rounds, " rounds")
    counter = 0
    first = True
    while counter is not rounds:
        if not color:
            local_color = get_random_color()
        for x in [4, 5, 6]:
            if x is 4:
                set_led(3, black, False, direction)
            if x is 6:
                set_led(3, local_color, False, direction)
            set_led(x, local_color, True, direction)
            speed_sleep(delay, speed)
            set_led(x, black, False, direction)

        for x in [2, 1, 0]:
            if x is 2:
                set_led(3, black, False, direction)
            if x is 0:
                set_led(3, local_color, False, direction)
            set_led(x, local_color, True, direction)
            speed_sleep(delay, speed)
            set_led(x, black, False, direction)
        counter += 1
        print(counter, "", end="", flush=True)
    print()

import copy
def diff_set_array(now, goal, direction=None):
    helper = copy.deepcopy(now)
    goal = copy.deepcopy(goal)
    #print("Now:  ", now)
    #print("Goal: ", goal)
    counter = 50
    while counter != 0:
        for x in range(7):
            for i in range(3):
                a = float(helper[x][i])
                b = float(goal[x][i])
                if abs(a - b) <= 2:
                    helper[x][i] = float(goal[x][i])
                elif helper[x][i] < float(goal[x][i]):
                    helper[x][i] += abs(a-b) / counter
                elif float(helper[x][i]) > float(goal[x][i]):
                    helper[x][i] -= abs(a-b) / counter

                helper[x][i] = int(helper[x][i])

        set_full_array(helper, direction)
        sleep(0.02)
        counter -= 1
    return list(helper)

def debug(direction=None):
    # while 1:
    #     #led = [red, orange, yellow, green, cyan, blue, white]
    #     led = [red, green, yellow, green, cyan, green, red]
    #     set_full_array(led, direction)
    #     sleep(0.5)
    # sleep(5)
    led = [red, red, red, red, red, red, red]
    sleep(0.5)
    set_full_array(led, direction)
    led = [green, green, green, green, green, green, green]
    sleep(0.5)
    set_full_array(led, direction)
    led = [blue, blue, blue, blue, blue, blue, blue]
    sleep(0.5)
    set_full_array(led, direction)


def rb(rounds=21, direction=None, delay=0.5, speed=10):
    if not direction:
        direction = random.choice(directions)
    print("RainBow, direction: ", direction)

    led = [red, orange, yellow, green, cyan, blue, white]
    set_full_array(led, direction)
    counter = 0
    while counter < rounds:
        goal = copy.deepcopy(led)
        goal.append(goal[0])
        goal.remove(goal[0])

        #print("Enterning vert_rb_loop")
        led = copy.deepcopy(diff_set_array(led, goal, direction))
        sleep(0.25) # Short delay better see the effect
        #print("New led is: ", led)
        counter += 1
        print(counter, "", end="", flush=True)
    print()
