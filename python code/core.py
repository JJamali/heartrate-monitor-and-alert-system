import serial
import tkinter as tk
import statistics

# set up fonts for pop up window stuff
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 80)
SMALL_FONT = ("Helvetica", 8)

# takes in string msg, returns pop up window when called with msg
def popupmsg(msg):
    popup = tk.Tk()
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
arr_check = False

# run indefinitely to constantly detect heartbeat
while True:

    input = ser.read()
    print(input)

    #======R wave======

    # check if in R wave
    if {{input > val}}:
        r_wave = True
    else:
        r_wave = False

    # detect R wave of heartbeat
    if r_wave:
        # remove first item from beat times and append current time
        beat_times.append(datetime.now())
        if len(beat_times) > 2:
            beat_times.pop(0)

        lastHR = 60000 / (beat_times[1] - beat_times[0])

        # add heartrate over last 30 beats to heartrates list
        heartrates.append(lastHR)
        if len(heartrates) > 29:
            heartrates.pop(0)

        # enter alarm logic only if we have collected enough heartrates
        if len(heartrates) > 30:
            if lastHR < 50:
                if statistics.mean(heartrates) > 40:
                    #mild alert
                else:
                    #high alert

            elif lastHR > 120:
                Enter high HR detection algorithm


            # ======arrhythmia======
            # if difference between last two beats exceeds 30%
            if math.abs((lastHR - heartrates[len(heartrates) - 2])/lastHR) > 0.3:
                arr_check = True


            # wait 15ms until R is over
            time.sleep(0.015)

    



