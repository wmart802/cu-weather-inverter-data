import tkinter

import databaseWriting as util

window = tkinter.Tk(classname='Inverter and Weather Data Logger')

runButton = Button(window, text='Run Database Writer')
runButton.grid(row=0, column=0)

window.mainloop
