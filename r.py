

from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk
import tkinter
from config.settings import version
import os



root = Tk()
root.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
root.geometry("400x400")
root.resizable(False, False)

# Getting all projects folders name from the directory 'projects' and saving it on a list - Rafael Sampaio
projects_list = [f.name for f in os.scandir("projects") if f.is_dir() ]

def open_project():
    selected_project_name = cmb_projects_list.get()
    messagebox.showinfo("IoTFogSim - %s"%(selected_project_name), "You're begin to start the %s simulation project. Just click the 'Ok' button." %(selected_project_name))
    root.destroy()






cmb_projects_list = ttk.Combobox(root, width="10", values=projects_list)
cmb_projects_list.place(relx="0.1",rely="0.1")

label_one = tkinter.Label(root,text="Select a project to open:")
label_one.place(relx="0.1",rely="0.04")

btn_open = ttk.Button(root, text="Open Project",command=open_project)
btn_open.place(relx="0.5",rely="0.1")

sep = ttk.Separator(root).place(relx="0.0", rely="0.2", relwidth=1)

label_two = tkinter.Label(root,text="Or create a new one and start.")
label_two.place(relx="0.1",rely="0.23")

label_three = tkinter.Label(root,text="Project name:")
label_three.place(relx="0.1",rely="0.3")

input_new_project_name = tkinter.Entry(root)
input_new_project_name.place(relx="0.4",rely="0.3")

btn_new = ttk.Button(root, text="Create new project and start it",command=None)
btn_new.place(relx="0.2",rely="0.4")

root.mainloop()







"""
from tkinter import *
import sys

class createProjectWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Project Name:")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.create_project_button=Button(top,text='Create and start',command=self.cleanup)
        self.create_project_button.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class mainWindow(object):
    
    def __init__(self,master):
        self.master=master
        self.new_project_button = Button(master,text="New project",command=self.popup)
        self.new_project_button.pack()
        self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
        self.b2.pack()

    def popup(self):
        self.w=createProjectWindow(self.master)
        self.new_project_button["state"] = "disabled" 
        self.master.wait_window(self.w.top)
        self.new_project_button["state"] = "normal"

    def entryValue(self):
        return self.w.value


if __name__ == "__main__":
    root=Tk()
    m=mainWindow(root)
    root.mainloop()

"""