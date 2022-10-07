# from twisted.internet.defer import inlineCallbacks
# from twisted.internet import reactor
# from twisted.internet.task import deferLater


# def sleep(secs):
#     return deferLater(reactor, secs, lambda: None)


# @inlineCallbacks
# def f():
#     print('writing for 5 seconds ...')
#     yield sleep(0.5)
#     print('now i am back ...')

import tkinter
import os


class ClusterDialog(tkinter.Toplevel):
    def __init__(self, parent, displayClass, clusterInfo, title = None):        
        tkinter.Toplevel.__init__(self, parent)
        self.transient(parent)
        #top = self.top = Toplevel(parent)
        if title:
            self.title(title)
        #set parent
        self.parent = parent
        #set class
        self.dClass = displayClass
        #dictionary to store the header data in 
        self.clusterInfo    = clusterInfo        
        self.geometry("300x300+10+10")

        #stores checkbox variables
        self.varList = None
        self.boxList = None
        self.name = None

        self.frameTopLevel  = tkinter.Frame(self,bd=2, width = 200,height=300)
        self.frameTopLevel.pack()

        self.buttonbox(self.frameTopLevel)
        self.frame = tkinter.Frame(self.frameTopLevel, width = 200,height=300)

        #frame=Frame(root,width=300,height=300)
        self.frame.grid(row=0,column=0)
        self.frame.pack()

        self.canvas=tkinter.Canvas(self.frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,1000))

        hbar = tkinter.Scrollbar(self.frame,orient=tkinter.HORIZONTAL)
        hbar.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        hbar.config(command=self.canvas.xview)
        vbar=tkinter.Scrollbar(self.frame,orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=tkinter.LEFT,expand=True,fill=tkinter.BOTH)
        self.frame.config(height = 100)
        self.body(self.canvas)
        self.canvas.config(width=300,height=300)
        self.grab_set()

ClusterDialog()