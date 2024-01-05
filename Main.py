
from tkinter import  Tk

import detector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image
import os


def Run_ui():
    root = Tk()
    root.title("Ube's Project")
    root.geometry("850x500")
    root.config(bg="white")
    app = detector.UI(root)

    app.mainloop()



Run_ui()

# e= GuiClass.MyGui(root)

# root.mainloop()