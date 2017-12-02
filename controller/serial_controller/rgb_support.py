from random import randint
from time import sleep
from serial import Serial

#ser = Serial('/dev/ttyACM0', 57600)  # open serial port
ser = Serial('/dev/ttyUSB0', 57600)

# Here is where we modify our local leds:
led = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

red = [250, 0, 0]
orange = [250, 127, 0]
yellow = [250, 250, 0]
green = [0, 250, 0]
blue = [0, 0, 250]
cyan = [139, 0, 250]
white = [250, 250, 250]
black = [0, 0, 0]

directions = ["right", "up", "down", "left"]
colors = [red, orange, yellow, green, cyan, blue, white]

def commit(direction=None):
    # This is the main function for

    # Array sent to Arduino:
    if not direction or direction is "right":
        values = [
            led[0][0], led[0][1], led[0][2],
            led[1][0], led[1][1], led[1][2],
            led[2][0], led[2][1], led[2][2],
            led[3][0], led[3][1], led[3][2],
            led[4][0], led[4][1], led[4][2],
            led[5][0], led[5][1], led[5][2],
            led[6][0], led[6][1], led[6][2],
        ]
    elif direction is "left":
        values = [
            led[6][0], led[6][1], led[6][2],
            led[5][0], led[5][1], led[5][2],
            led[4][0], led[4][1], led[4][2],
            led[3][0], led[3][1], led[3][2],
            led[2][0], led[2][1], led[2][2],
            led[1][0], led[1][1], led[1][2],
            led[0][0], led[0][1], led[0][2],
        ]
    elif direction is "up":
        values = [
            led[3][0], led[3][1], led[3][2],
            led[2][0], led[2][1], led[2][2],
            led[1][0], led[1][1], led[1][2],
            led[0][0], led[0][1], led[0][2],
            led[1][0], led[1][1], led[1][2],
            led[2][0], led[2][1], led[2][2],
            led[3][0], led[3][1], led[3][2],
        ]
    elif direction is "down":
        values = [
            led[0][0], led[0][1], led[0][2],
            led[1][0], led[1][1], led[1][2],
            led[2][0], led[2][1], led[2][2],
            led[3][0], led[3][1], led[3][2],
            led[2][0], led[2][1], led[2][2],
            led[1][0], led[1][1], led[1][2],
            led[0][0], led[0][1], led[0][2],
        ]


    #print(values)
    serial_write(values)

def serial_write(values):
    #ser.reset_input_buffer()
    while ser.in_waiting:
    #if ser.in_waiting:
        response = ser.readline()
        print(response)
        sleep(0.02)
    values.insert(0, 255)
    values.append(254)
    #print(values)
    ser.write(bytearray(values))
    #print("Serial sent")
    while ser.in_waiting:
    #if ser.in_waiting:
        response = ser.readline()
        print(response)
        sleep(0.02)

def set_full_array(values, direction=None):
    global led
    led = values
    commit(direction)

# LED number + color[array]
def set_led(x, i, send=True, direction=None):
    global led
    led[x][0] = i[0]
    led[x][1] = i[1]
    led[x][2] = i[2]
    if send:
        commit(direction)

def set_all(color=None):
    global black
    global led
    if not color:
        # color = black
        color = get_random_color()
    for x in range(7):
        led[x][0] = color[0]
        led[x][1] = color[1]
        led[x][2] = color[2]
    commit()

old_random = None
def get_random_color():
    global old_random
    new_random = randint(0,6)
    while new_random is old_random:
        new_random = randint(0,6)
    old_random = new_random
    return colors[new_random]

def slow_fade_led(i, new_value = []):
    #print("Fading ", led[i], " to: ", new_value)
    tests = [False, False, False]
    while False in tests:
        for x in range(3):
            if abs(led[i][x] - new_value[x]) > 5:
                if led[i][x] < new_value[x]:
                    led[i][x] += slow
                else:
                    led[i][x] -= slow
            else:
                tests[x] = True

        sleep(0.1)
        commit()

def fade_led(i, new_value, speed=5):
    tests = [False, False, False]
    for x in range(3):
        if abs(led[i][x] - new_value[x]) > speed:
            if led[i][x] < new_value[x]:
                led[i][x] += speed
            else:
                led[i][x] -= speed
        else:
            tests[x] = True
    if False in tests:
        return False
    else:
        return True

def slow_fade_all(color=False):
    #set_all()
    if not color:
        color = get_random_color()

    print("Fading to: ", color)
    tests = [False, False, False, False, False, False, False]
    while False in tests:
        for x in range(7):
            tests[x] = fade_led(x, color, 1)
        sleep(0.01)
        commit()
    print("Done")

def speed_sleep(delay, speed):
    print("Base delay: ", delay, "Speed: ", speed.value)
    sleep_delay = delay / speed.value
    sleep(sleep_delay)
