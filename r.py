import tkinter as tk
import time


def GetDateTime():
    # Get current date and time in ISO8601
    # https://en.wikipedia.org/wiki/ISO_8601
    # https://xkcd.com/1179/
    return (time.strftime("%Y%m%d", time.gmtime()),
            time.strftime("%H%M%S", time.gmtime()),
            time.strftime("%Y%m%d", time.localtime()),
            time.strftime("%H%M%S", time.localtime()))


class Application(tk.Frame):

    def __init__(self, master):

        fontsize = 12
        textwidth = 9

        tk.Frame.__init__(self, master)
        self.pack()

        tk.Label(self, font=('Helvetica', fontsize), bg='#be004e', fg='white', width=textwidth,
                 text='Local Time').grid(row=0, column=0)
        self.LocalDate = tk.StringVar()
        self.LocalDate.set('waiting...')
        tk.Label(self, font=('Helvetica', fontsize), bg='#be004e', fg='white', width=textwidth,
                 textvariable=self.LocalDate).grid(row=0, column=1)

        tk.Label(self, font=('Helvetica', fontsize), bg='#be004e', fg='white', width=textwidth,
                 text='Local Date').grid(row=1, column=0)
        self.LocalTime = tk.StringVar()
        self.LocalTime.set('waiting...')
        tk.Label(self, font=('Helvetica', fontsize), bg='#be004e', fg='white', width=textwidth,
                 textvariable=self.LocalTime).grid(row=1, column=1)

        tk.Label(self, font=('Helvetica', fontsize), bg='#40CCC0', fg='white', width=textwidth,
                 text='GMT Time').grid(row=2, column=0)
        self.nowGdate = tk.StringVar()
        self.nowGdate.set('waiting...')
        tk.Label(self, font=('Helvetica', fontsize), bg='#40CCC0', fg='white', width=textwidth,
                 textvariable=self.nowGdate).grid(row=2, column=1)

        tk.Label(self, font=('Helvetica', fontsize), bg='#40CCC0', fg='white', width=textwidth,
                 text='GMT Date').grid(row=3, column=0)
        self.nowGtime = tk.StringVar()
        self.nowGtime.set('waiting...')
        tk.Label(self, font=('Helvetica', fontsize), bg='#40CCC0', fg='white', width=textwidth,
                 textvariable=self.nowGtime).grid(row=3, column=1)

        tk.Button(self, text='Exit', width=10, bg='#FF8080',
                  command=root.destroy).grid(row=4, columnspan=2)

        self.gettime()
    pass

    def gettime(self):
        gdt, gtm, ldt, ltm = GetDateTime()
        gdt = gdt[0:4] + '/' + gdt[4:6] + '/' + gdt[6:8]
        gtm = gtm[0:2] + ':' + gtm[2:4] + ':' + gtm[4:6] + ' Z'
        ldt = ldt[0:4] + '/' + ldt[4:6] + '/' + ldt[6:8]
        ltm = ltm[0:2] + ':' + ltm[2:4] + ':' + ltm[4:6]
        self.nowGtime.set(gdt)
        self.nowGdate.set(gtm)
        self.LocalTime.set(ldt)
        self.LocalDate.set(ltm)

        self.after(100, self.gettime)
       # print (ltm)  # Prove it is running this and the external code, too.
    pass


root = tk.Tk()
root.wm_title('Temp Converter')
app = Application(master=root)

w = 200  # width for the Tk root
h = 125  # height for the Tk root

# get display screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for positioning the Tk root window

# centered
#x = (ws/2) - (w/2)
#y = (hs/2) - (h/2)

# right bottom corner (misfires in Win10 putting it too low. OK in Ubuntu)
x = ws - w
y = hs - h - 35  # -35 fixes it, more or less, for Win10

# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.mainloop()
