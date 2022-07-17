import serial
import tkinter as tk
import statistics

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
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'PORTNAME' # note: this changes with different environments


# list of the previous 30 beat times
beat_times = []

# list of previous 29 intervals between beats
beat_intervals = []

# list of heartrates 
heartrates = []

r_wave = False
off_check = False

# run indefinitely to constantly detect heartbeat
while True:

    input = ser.read()
    # print(input)

    #======R wave======

    # check if in R wave
    if {{input > val}}:
        r_wave = True
    else:
        r_wave = False
        # wait 10ms
        time.sleep(0.010)

    if r_wave:
        # remove first item from beat times and append current time
        beat_times.append(datetime.now())
        if len(beat_times) > 2:
            beat_times.pop(0)

        lastHR = 60000 / (beat_times[1] - beat_times[0])

        # add heartrate over last 30 beats to heartrates list
        heartrates.append(lastHR)
        if len(heartrates) > 15:
            heartrates.pop(0)

        # enter alarm logic only if we have collected enough heartrates
        if len(heartrates) > 15:
            if lastHR < 50:
                if 40 < statistics.mean(heartrates) < 50:
                    # mild alert
                    popupmsg("low heart rate detected", grey)
                elif statistics.mean(heartrates) < 40:
                    # high alert
                    popupmsg("low heart rate detected - dangerous", red)

            elif lastHR > 120:
                if 120 < statistics.mean(heartrates) < 130:
                    # mild alert
                    popupmsg("high heart rate detected", grey)
                elif statistics.mean(heartrates) > 130:
                    # high alert
                    popupmsg("low heart rate detected - dangerous", red)

            # ======arrhythmia======
            # if difference between last two beats exceeds 30%
            if math.abs((lastHR - heartrates[len(heartrates) - 2])/lastHR) > 0.3:

                arrhythmic_beats = 0
                for i in range(len(heartrates)):
                    if math.abs(heartrates(i + 1) - heartRates(i)) / heartrates(i) > 0.3:
                        arrhythmic_beats += 1

                if arrhythmic_beats > 6:
                    # high alert
                    popupmsg("arrhythmia detected - dangerous", red)
                elif arrhythmic_beats > 4:
                    # low alert
                    popupmsg("mild arrhythmia detected", grey)


            # ======off check======
            if lastHR == 0:
                off_check = True

                if sum(heartrates[5:14]) == 0:
                    popupmsg("device removed", grey)
                    off_check = False

            # wait 15ms until R wave is over
            time.sleep(0.015)
