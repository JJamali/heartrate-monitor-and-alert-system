import serial
import tkinter as tk

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'PORTNAME'



LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 80)
SMALL_FONT = ("Helvetica", 8)



# list of the previous 30 beat times
beat_times = []

# list of previous 29 intervals between beats
beat_intervals = []

# list of heartrates 
heartrates = []

# detect R wave of heartbeat

if R:
    # remove first item from beat times and append current time
    beat_times.append(datetime.now())
    beat_times.pop(0)
    
    # add heartrate over last 30 beats
    heartrates.append((beat_times[len(beat_times)] - beat_times[0]) / 30) 
    



