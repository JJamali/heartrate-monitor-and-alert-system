import serial
import tkinter as tk
import statistics
import time
from datetime import datetime
import math

# set up fonts for pop up window stuff
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 80)
SMALL_FONT = ("Helvetica", 8)

# takes in string msg, returns pop up window when called with msg
# color dictates background color
def popupmsg(msg, color):
    popup = tk.Tk()
    popup.configure(bg=color)
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# connect python to arduino serial readings
ser = serial.Serial('COM3', 9600, timeout=1)
#ser.baudrate = 9600
#ser.port = 'COM3' # note: this changes with different environments
#ser.open()
print(ser.name)


# list of the previous 30 beat times
beat_times = []

# list of previous 29 intervals between beats
beat_intervals = []

# list of heartrates 
heartrates = []

lastHR = 0

r_wave = False

# run indefinitely to constantly detect heartbeat
while True:

    try:
        input = ser.readline()
    except Exception:
        print("unable to read line")
    
    # code to extract number from input data
    # use try-except to omit any non-numerical data and prevent crashes
    num = ""
    print(input)
    for c in str(input):
        if c.isdigit():
            num += c
    if num != "":
        input = int(num)
    else:
        input = 0
        
    print("cleaned input = " + str(input))
     #======R wave======

    # check if in R wave
    if 600 < input < 700:
        r_wave = True
    else:
        r_wave = False
        # wait 10ms
        time.sleep(0.010)
        

    if r_wave:
        print("R wave")
        # remove first item from beat times and append current time
        beat_times.append(datetime.now())
        if len(beat_times) > 2:
            beat_times.pop(0)
            
            if (beat_times[1] - beat_times[0]).total_seconds() != 0:
                lastHR = 60000 / ((beat_times[1] - beat_times[0]).total_seconds() * 1000)
            else: # just give it something really high
                lastHR = 200
        # add heartrate over last 30 beats to heartrates list
        heartrates.append(lastHR)
        if len(heartrates) > 15:
            heartrates.pop(0)

        # enter alarm logic only if we have collected enough heartrates
        if len(heartrates) > 15:
            if lastHR < 50:
                print("enter low check")
                if 40 < statistics.mean(heartrates) < 50:
                    # mild alert
                    popupmsg("low heart rate detected", "grey")
                elif statistics.mean(heartrates) < 40:
                    # high alert
                    popupmsg("low heart rate detected - dangerous", "red")

            elif lastHR > 120:
                print("enter high check")
                if 120 < statistics.mean(heartrates) < 130:
                    # mild alert
                    popupmsg("high heart rate detected", "grey")
                elif statistics.mean(heartrates) > 130:
                    # high alert
                    popupmsg("low heart rate detected - dangerous", "red")

            # ======arrhythmia======
            # if difference between last two beats exceeds 30%
            if math.abs((lastHR - heartrates[len(heartrates) - 2])/lastHR) > 0.3:
                print("enter arr check")
                arrhythmic_beats = 0
                for i in range(len(heartrates)):
                    if math.abs(heartrates(i + 1) - heartrates(i)) / heartrates(i) > 0.3:
                        arrhythmic_beats += 1

                if arrhythmic_beats > 6:
                    # high alert
                    popupmsg("arrhythmia detected - dangerous", "red")
                elif arrhythmic_beats > 4:
                    # low alert
                    popupmsg("mild arrhythmia detected", "grey")


    # ======off check======
    if lastHR == 0 and sum(heartrates[5:14]) == 0 and len(heartrates) > 10:
        print("enter off check")
        print(heartrates)
        popupmsg("device removed", "blue")
