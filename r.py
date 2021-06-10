import tkinter as tk


class Menu:
    def __init__(self, parent, **kwargs):
        self._popup = None
        self._menubutton = []
        self.parent = parent

        self.parent.bind('<Button-1>', self.on_popup)

    def on_popup(self, event):
        w = event.widget
        x, y, height = self.parent.winfo_rootx(), self.parent.winfo_rooty(), self.parent.winfo_height()

        self._popup = tk.Toplevel(self.parent.master, bg=self.parent.cget('bg'))
        self._popup.overrideredirect(True)
        self._popup.geometry('+{}+{}'.format(x, y + height))

        for kwargs in self._menubutton:
            self._add_command(**kwargs)

    def add_command(self, **kwargs):
        self._menubutton.append(kwargs)

    def _add_command(self, **kwargs):
        command = kwargs.pop('command', None)

        menu = self.parent
        mb = tk.Menubutton(self._popup, text=kwargs['label'],
                           bg=menu.cget('bg'),
                           fg=menu.cget('fg'),
                           activebackground=menu.cget('activebackground'),
                           activeforeground=menu.cget('activeforeground'),
                           borderwidth=0,
                           )
        mb._command = command
        mb.bind('<Button-1>', self._on_command)
        mb.grid()

    def _on_command(self, event):
        w = event.widget
        print('_on_command("{}")'.format(w.cget('text')))

        self._popup.destroy()

        if w._command is not None:
            w._command()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x200")

        style = {'bg': "#102A43", 'fg': "white", 
                 'activebackground': "#243B53", 'activeforeground': "white",
                 'borderwidth': 0}

        menu1 = tk.Menubutton(self, text="Menu1", **style)
        submenu1 = Menu(menu1)
        submenu1.add_command(label="Option 1.1")
        submenu1.add_command(label="Option 1.2")
        menu1.grid(row=0, column=0)

        menu2 = tk.Menubutton(self, text="Menu2", **style)
        submenu2 = Menu(menu2)
        submenu2.add_command(label="Option 2.1")
        submenu2.add_command(label="Option 2.2")
        menu2.grid(row=0, column=2)


if __name__ == "__main__":
    App().mainloop()