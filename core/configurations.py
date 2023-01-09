import tkinter
from tkinter import PhotoImage
from twisted.internet import tksupport
from twisted.python import log

from core.pre_start import load_nodes, load_humans, load_appliances
from core.simulationcore import SimulationCore
import json
import os
from tkinter import ttk
from tkinter import messagebox
from config.settings import version

from core.functions import configure_logger
from core.functions import get_default_interface

from twisted.internet import task

from multiprocessing import Process

from twisted.internet import reactor


import time


from pathlib import Path


def config():
    # para que uma aplicação com tkinter possa usar varias janelas é preciso uma instancia de tkinter.Tk()
    # que será o pai. As janelas(filhas) devem ser cirdas com tkinter.Toplevel() - Rafael Sampaio
    root = tkinter.Tk()
    # escondendo a instancia vazia de tk() para evitar a exibição desnecessária - Rafael Sampaio
    root.withdraw()

    simulation_core = SimulationCore()
    simulation_core.start_clock()

    # initialization_screen(simulation_core)
    reactor.callFromThread(initialization_screen, simulation_core)
    
    # generates results when reactor stopped via command line (CRTL+C)
    reactor.addSystemEventTrigger('before', 'shutdown', simulation_core.before_close)


def initialization_screen(simulation_core):
    window = tkinter.Toplevel()
    tksupport.install(window)
    window.title(
        "IoTFogSim %s - An Event-Driven Network Simulator" % (version))
    window.geometry("833x469")
    window.resizable(False, False)

    # Setting window icon. - Rafael Sampaio
    window.iconphoto(True, PhotoImage(
        file='graphics/icons/iotfogsim_icon.png'))

    # returns a list with all the subdirectoys in a folder -  Rafael Sampaio
    def load_projects(directory):
        return [f.name for f in os.scandir(directory) if f.is_dir()]

    def open_project(window, simulation_core):
        selected_project_name = cmb_projects_list.get()
        # messagebox.showinfo("IoTFogSim - %s"%(selected_project_name), "You're begin to start the %s simulation project. Just click the 'Ok' button." %(selected_project_name))

        if selected_project_name == '':
            messagebox.showwarning('No project', 'Please, select a project!')
        else:
            simulation_core.project_name = selected_project_name

            # Configuring log - Rafael Sampaio
            log_path = "projects/"+selected_project_name+"/"
            configure_logger(log_path, selected_project_name)

            resizable = None
            with open('projects/'+selected_project_name+'/settings.json', 'r') as settings:
                data = json.loads(settings.read())
                settings = data['settings']
                resizable = settings['resizeable']
            
            if 'global_seed' in settings:
                simulation_core.global_seed = settings['global_seed']
            else:
                simulation_core.global_seed = None
                
            if 'currency_prefix' in settings:
                simulation_core.currency_prefix = settings['currency_prefix']
            else:
                simulation_core.currency_prefix = "USD"
                
            if 'kwh_price' in settings:
                simulation_core.kwh_price = settings['kwh_price']
            else:
                simulation_core.kwh_price = 0.99

            simulation_core.create_simulation_canvas(resizable)
            if 'scene_adapter' in settings:
                simulation_core.build_scene_adapter(
                    settings['scene_adapter'])
            
            load_nodes(selected_project_name, simulation_core)
            load_appliances(selected_project_name, simulation_core)
            load_humans(selected_project_name, simulation_core)

            window.destroy()
            window.update()

    def creat_project(window, new_project_name, simulation_core):
        try:
            if new_project_name == '':
                messagebox.showwarning(
                    'Invalid Project Name', 'Project name can not be empty!')
            else:
                os.makedirs("projects/%s" % (new_project_name))

                # Configuring log - Rafael Sampaio
                log_path = "projects/"+new_project_name+"/"
                configure_logger(log_path, new_project_name)

                simulation_core.project_name = new_project_name

                # creating the node.json file into the project directory - Rafael Sampaio
                nodes_file = "projects/%s/nodes.json" % (new_project_name)
                if not os.path.exists(nodes_file):
                    with open(nodes_file, 'w') as file:
                        print("{}", file=file)

                # creating the settings.json file into the project directory - Rafael Sampaio
                settings_file = "projects/%s/settings.json" % (
                    new_project_name)
                if not os.path.exists(settings_file):
                    with open(settings_file, 'w') as file:
                        print('{"settings":{"resizeable": true}}', file=file)

                # default resizeable screen is true for new projects - Rafael Sampaio
                simulation_core.create_simulation_canvas(resizeable=True)
                load_nodes(new_project_name, simulation_core)

                window.destroy()
                window.update()

        except FileExistsError:
            # if the directory already exists - Rafael Sampaio
            messagebox.showerror("IoTFogSim - Error while create project",
                                 "The project %s already exists!" % (new_project_name))

    # Getting all projects folders name from the directory 'projects' and saving it on a list - Rafael Sampaio
    projects_list = load_projects("projects")

    # configure backgroud image - Rafael Sampaio
    bg_image = PhotoImage(file="graphics/images/background2.png")
    x = tkinter.Label(window, image=bg_image)
    x.place(relx="0.0", rely="0.0")
    x.img = bg_image

    cmb_projects_list = ttk.Combobox(window, width="20", values=projects_list)
    cmb_projects_list.place(relx="0.1", rely="0.35")

    label_one = tkinter.Label(window, text="Select a project to open:")
    label_one.place(relx="0.1", rely="0.3")

    btn_open = ttk.Button(window, text="Open Project",
                          command=lambda: open_project(window, simulation_core))
    btn_open.place(relx="0.32", rely="0.34")

    sep = ttk.Separator(window).place(relx="0.0", rely="0.45", relwidth=1)

    label_two = tkinter.Label(window, text="Or create a new one and start.")
    label_two.place(relx="0.1", rely="0.5")

    label_three = tkinter.Label(window, text="Project name:")
    label_three.place(relx="0.1", rely="0.55")

    input_new_project_name = tkinter.Entry(window)
    input_new_project_name.place(relx="0.1", rely="0.6")

    btn_new = ttk.Button(window, text="Create new project and start it", command=lambda: creat_project(
        window, input_new_project_name.get(), simulation_core))
    btn_new.place(relx="0.1", rely="0.65")
