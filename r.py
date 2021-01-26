from tkinter import *

# New Tkinter
root = Tk()
sw = str(root.winfo_screenwidth())

# Function for new toplevel
def new_wdow():
    w = Toplevel(root)
    w.geometry("0x0+" + sw + "+0")
    w.state('zoomed')
    w.overrideredirect(1)
    Label(w, text='Hello Secondary Display').pack()

# Make button in main window
Button(root, text="Hello", command=new_wdow).pack()

root.mainloop()


# ,
#                     {
#                         "id":0,
#                         "name": "wsn_sink",
#                         "icon": "sink_icon",
#                         "coverage_area_radius": 100,
#                         "is_wireless": true,
#                         "application": "applications.wsnapp.SinkApp",
#                         "x": 202,
#                         "y": 1152
#                     }