import pyautogui
import serial
import keyboard
import time

comport = "COM5"
baudrate = 115200
d1 = {
    "x_off": 0,
    "correct_state": False,
    "precise": False,
    "invert_x": False,
    "enbl": True,
    "loop": True,
}


def disable(*_):
    d1["loop"] = False


def disable_soft(*_):
    d1["enbl"] = not d1["enbl"]


def correct_off_state(*_):
    d1["correct_state"] = True


def precise_state():
    d1["precise"] = not d1["precise"]


def data_sp(s):
    a = []
    for i in str(s).split():
        try:
            a.append(float(i))
        except:
            return
    return a


def get_data():
    global data
    ser = serial.Serial(comport, baudrate, timeout=0.2)
    while True:
        tdata = ser.readline().decode().strip()
        if tdata and d1["enbl"]:
            try:
                tdata = [float(x) for x in tdata.split()]
                data = tdata
                # print(tdata)
            except:
                print(tdata)


def calibrate(temp, x):
    if temp == 0:
        d1["x_off"] = x - prev
        prev.clear()
        temp = -1
        d1["correct_state"] = False
        print(d1)
    elif temp == -1:
        prev = x
        temp = 10
        time.sleep(1)
        return True
    else:
        temp -= 1
        return True


dist = 0.1


def mouse_x3(x_val, x1, x2, y1, y2):
    # linear interpolation
    # -80 , 80 , 0 , 1920
    return y1 + (x_val - x1) * (y2 - y1) / (x2 - x1)


def mov_mouse(x):
    pyautogui.moveTo(x=x, duration=0.1)


def mouse_click(b, pr):
    if b != pr:
        print("b:", b)
        if b == 0:
            pyautogui.moveTo(y=100, duration=0.01)
        elif b == 1:
            pyautogui.moveTo(y=900, duration=0.01)
        elif b == 2:
            pyautogui.moveTo(y=100, duration=0.01)
        else:
            pyautogui.moveTo(y=960, duration=0.01)
        pr = b
    else:
        pass


def deNoise(x1, x2, y1, y2):
    # TODO de noising of input
    # increase rate of input
    pass


# TODO use multithredding to speed up , optimize code
input_data = []


def read():
    ser = serial.Serial(comport, baudrate, timeout=0.1)
    data = ser.readline().decode().strip()
    if data:
        try:
            data = data.split()
            data = f"{float(data[0]):.2f} {float(data[1]):.2f} {data[2]} {data[3]} {data[4]}"
            with open("inp.txt", "a") as f:
                f.write()
        except:
            print(data)


def main():
    curr = []
    prev = []
    temp = -1
    clickpr = 0
    ser = serial.Serial(comport, baudrate, timeout=0.2)
    # 1/timeout is the frequency at which the port is read
    keyboard.add_hotkey("`", disable)
    keyboard.add_hotkey("/", disable_soft)
    keyboard.add_hotkey("*", correct_off_state)
    keyboard.add_hotkey(".", precise_state)
    pyautogui.PAUSE = 0.001
    while d1["loop"]:
        # s1 = time.time_ns()
        try:
            data = ser.readline().decode().strip()
            if data and d1["enbl"]:
                curr = data_sp(data)

                x_angle = (curr[0]) / 1.2
                # print(x_angle,y_angle)
                if d1["precise"]:
                    x_angle /= 2
                if d1["invert_x"]:
                    x_angle *= -1
                x = (mouse_x3(x_angle, 65, -60, 0, 1920)) - d1["x_off"]
                if d1["correct_state"]:
                    c = calibrate(temp, x)
                    if c:
                        continue
                # print(f"{x:.2f} {y:.2f}")
                # s2 = time.time_ns()
                mov_mouse(x)
                print(curr)
                mouse_click(curr[-1], clickpr)
                # s3 = time.time_ns()
                # print((s2-s1)/1000000,(s3-s2)/1000000,(s3-s1)/1000000)
                # print(time.perf_counter())
                prev = curr.copy()
        except:
            print("err")
            # print(time.time_ns()-s1)


main()
