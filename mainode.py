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

