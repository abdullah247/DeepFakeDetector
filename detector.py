import threading,time
from multiprocessing.pool import Pool

from tkinter import *
from tkinter import filedialog, ttk
import asyncio

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image, ImageOps
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import numpy as np
from skimage import transform
from MyClassifer import MyModel


class UI(Frame):
    bgTheme ="#2196f3"
    fgTheme ="white"
    confidenceColor="Red"
    mainBackground="white"
    myboldfont= ("Arial", 25, "bold")
    myFont= ("Arial", 12, "normal")



    def __init__(self, parent):
        self.model = MyModel()
        self.model.load('mymodel.h5')
        self.dataGenerator = ImageDataGenerator(rescale=1. / 255)
        self.xx = 0
        self.yy = 0

        # Instantiating generator to feed images through the network


        self.parent = parent
        Frame.__init__(self, parent)
        self.create_widgets(parent)


    def create_widgets(self, root):
        #first


        # self.confilabel.pack()

        self.f1 = Frame(root, bg="white")
        # # self.f1.place(x=300, y=70)
        self.f1.configure(height=15, width=15)
        self.f1.pack(side=RIGHT)

        PieChartLabels = ['Real', 'Fake']
        PieChartValues = [50, 50]

        self.chart2xLables =["0%-20%","21%-40%","41%-60%","61%-80%","81%-100%"]
        value2= [100,100,100,100,100]

        # pie chart
        self.fig = Figure(figsize=(3,3), dpi=100)  # create a figure object
        self.fig.set_size_inches(3, 2)

        self.ax = self.fig.add_subplot(111)  # add an Axes to the figure
        self.ax.clear()

        self.ax.pie(PieChartValues, radius=1, labels=PieChartLabels, autopct='%0.2f%%', shadow=True, )
        self.chart1 = FigureCanvasTkAgg(self.fig, root)
        self.chart1.get_tk_widget().place(x=2,y=70)

        #column  chart
        self.fig2 = Figure(figsize=(3, 3), dpi=100)  # create a figure object
        self.fig2.set_size_inches(3, 2)

        # ax2
        self.ax2 = self.fig2.add_subplot(111)  # add an Axes to the figure
        self.ax2.clear()

        self.ax2.bar(self.chart2xLables, value2, width = .5 )
        self.ax2.tick_params(axis='x', labelsize=5)
        self.chart2 = FigureCanvasTkAgg(self.fig2, root)
        self.chart2.get_tk_widget().place(x=2, y=270)

        # image
        self.image1 = Image.open(r"C:\Users\aliab\Downloads\archive\real_and_fake_face\training_real\real_00002.jpg")
        self.image1=  self.image1.resize((250, 250), Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.image1,size=(259,250))
        self.labelImage = Label(root,image=self.test,width=250,height=250,bg="blue")
        self.labelImage.image = self.test

        self.labelImage.place(x=340,y=70)

        # listbox
        self.listbox = Listbox(self.f1, height=20, width=15,
                               bg=self.mainBackground,
                               activestyle='dotbox',
                               font=self.myFont,
                               fg="black")
        # self.f1.place(x=700, y=30)
        self.listbox.pack(side="right",fill=Y)

        # Select button
        # Confidence Label
        self.st1=StringVar()
        self.st1.set("0%")

        self.st2 = StringVar()
        self.st2.set("")

        #progress bar
        self.p1 = ttk.Progressbar(root, length=300, style="blue.Horizontal.TProgressbar", cursor='spider',
                             mode="determinate", orient=HORIZONTAL)
        self.p1.place(x=320,y=380)

        self.confilabel = Label(root, textvariable=self.st1, bg=self.fgTheme, fg=self.confidenceColor,
                                font=self.myboldfont)
        self.confilabel.place(x=440,y=330)

        self.realfake = Label(root, textvariable=self.st2, bg=self.fgTheme, fg=self.confidenceColor,
                                font=self.myboldfont)
        self.realfake.place(x=440, y=20)

        self.selectbutton = Button(root, text="Select", bg=self.bgTheme, fg=self.fgTheme,command=self.insertInListBox)
        self.selectbutton.place(x=440,y=420)



        self.DeleteButton = Button(root, text="Delete", bg="Red", fg=self.fgTheme,
                                   command=self.deleteme)
        self.DeleteButton.place(x=750,y=450)

        self.listbox.bind("<<ListboxSelect>>", self.callback)


        self.scrollbar = Scrollbar(self.f1,orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        # ani = animation.FuncAnimation(self.fig, self.animate, 10)
        # self.label.pack()
        # animation
        # self.ani =animation.FuncAnimation(self.fig,self.animate,interval=2000)

    async def updateChart(self):
        x=0
        y=0
        x2,x4,x6,x8,x0 = 0,0,0,0,0

        k=0
        for i, listbox_entry in enumerate(self.listbox.get(0, END)):
            # await asyncio.sleep(1)
            if i% 3 == 1 :
                k+=1

                np_image = Image.open(os.path.join(self.address, listbox_entry))
                np_image = ImageOps.flip(np_image)
                np_image = np.array(np_image).astype('float32') / 255
                np_image = transform.resize(np_image, (96, 96, 3))
                np_image = np.expand_dims(np_image, axis=0)
                # time.sleep(2)
                print("Predicting all values for pie chart")
                val=self.model.predict(np_image)[0][0]

                if ( val> .5):
                    x+=1
                    if val>.8:
                        x8+=1
                    elif val>.6:
                        x6+=1
                    else:
                        x4+=1
                else:
                    y += 1
                    if val>.40:
                        x4+=1
                    elif val>.20:
                        x2+=1
                    else:
                        x0+=1

                if k>40:
                    break;

                stockListExp = ['Real', 'Fake']
                tt=x+y
                print(val)

                stockSplitExp = [ round(x/tt*100,3),  round(y/tt*100,3)]
                self.ax.clear()
                self.ax.pie(stockSplitExp, radius=1, labels=stockListExp, autopct='%0.2f%%', shadow=True, )
                self.chart1.draw_idle()

                value2=[round(x0/tt*100,3),  round(x2/tt*100,3),round(x4/tt*100,3),  round(x6/tt*100,3),round(x8/tt*100,3)]
                self.ax2.clear()
                self.ax2.bar(self.chart2xLables, value2, width=.5)
                self.ax2.tick_params(axis='x', labelsize=5)
                self.chart2.draw_idle()
                self.parent.update()

        # self.chart1.get_tk_widget().pack(side=LEFT)


    def deleteme(self):
        global things
        # Delete from Listbox
        selection = self.listbox.curselection()
        self.listbox.delete(selection[0])

        # Delete from list that provided it
        # value = eval(self.listbox.get(selection[0]))
        # ind = things.index(value)
        # del (things[ind])

    def syncfunction(self):
        self.address = filedialog.askdirectory()
        if len(self.address) > 1:
            self.listbox.delete(0, 'end')
            self.generator = self.dataGenerator.flow_from_directory(
                self.address,
                target_size=(256, 256),
                batch_size=1,
                class_mode='binary')
            for filename in os.listdir(self.address):
                self.listbox.insert(END, filename)

        self.scrollbar.config(command=self.listbox.yview)


    def insertInListBox(self):
       self.syncfunction()
       asyncio.run(self.updateChart())

        # asyncio.run(self.updateChart())

    # def insertInListBox(self):
    #     for i in range(100):
    #         self.listbox.insert(END, i)
    #     # self.listbox.config(yscrollcommand=self.scrollbar.set)
    #     # self.scrollbar.config(command=self.listbox.yview)

    def ClickedSelected(self):
        print("")

    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.image1 = Image.open(os.path.join(self.address,data))
            self.image1 = self.image1.resize((250, 250), Image.ANTIALIAS)
            self.test = ImageTk.PhotoImage(self.image1, size=(250, 250))
            self.labelImage.config(image=self.test)
            self.labelImage.image=self.test
            np_image = Image.open(os.path.join(self.address,data))
            np_image = ImageOps.flip(np_image)
            np_image = np.array(np_image).astype('float32') / 255
            np_image = transform.resize(np_image, (96, 96, 3))
            np_image = np.expand_dims(np_image, axis=0)
            stockSplitExp=[3,97]
            # input_arr = np.array([input_arr])
            # print(f"{self.meso.predict(np_image)[0][0]:.4f}")
            val=self.model.predict(np_image)[0][0] * 100
            self.p1["value"]=val
            self.st1.set(f"{val:.0000f} %")
            if (self.model.predict(np_image)[0][0]>.5):
                self.st2.set("Real")
            else:
                self.st2.set("Fake")


            self.parent.update()
            print(data)
        else:
            print("")


