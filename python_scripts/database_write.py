# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 04:40:56 2019

@author: Lab


Corner cases:
    what if the computer turns off and misses some of the logged data?
    what if the inverter turns off and doesn't log data, but the script continues to run?
    What if the inverter but not the weather station turns off (or vice versa)?
    
TODO: when the script starts, if there is more recent logged data than the database contains insert those vals
TODO: compare timestamps between inverter log and wx log, normalize to one timestamp

"""

# -*- coding: utf-8 -*-
from tkinter import Tk, Button, Label, filedialog
#import time
import sys

import database_write_util as util
import RepeatedTimer as timer

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

#time_hour = time.strftime("%H",time.localtime())
#time_min  = time.strftime("%M",time.localtime())
#time_sec  = time.strftime("%S",time.localtime())
#time_year  = time.strftime("%Y",time.localtime())
#time_month = time.strftime("%m",time.localtime())
#time_day   = time.strftime("%d",time.localtime())


window = Tk()

path_weather_file  = ""

index_inverter_file_time = 2
index_inverter_file_start = 9



def startScriptButton():
    global rt
    
    if util.inverterLogDirPath: #& util.weatherXmlPath):
        
        util.getMissedInverterData()
        util.firstRunFlag = 0
        rt.start()
        util.processFiles()
    

def forceStopButton():
    global rt
    rt.stop()    
    print("force stop")
    
def on_closing():    
    window.destroy()
    print("exiting gui")
    try:
        rt.stop()
    except:
        pass
    try:
        sys.exit()
    except:
        pass
    
def openInverterLogDirButton():
    window.withdraw()
    util.inverterLogDirPath = filedialog.askdirectory()
    window.deiconify() 
    print('Inverter Log Directory: ' + util.inverterLogDirPath)
    util.chooseInverterLogFile()
    
    
def openXMLFileButton():
    window.withdraw()
    util.weather_xml_file_path = filedialog.askopenfilename()
    window.deiconify() 
    print("xml file path selected")
     
    
    
    # global path_xml_file, sql_database_array_xml
    # global data_xml_dewpoint, data_xml_pressure, data_xml_humidity
    # global data_xml_temp, data_xml_degrees, data_xml_windspeed, data_xml_time
    # tree = ElementTree.parse(path_xml_file)
    # root = tree.getroot()
        
    # for child in root:
        # if child.tag == "temp_c":
            # data_xml_temp = child.text    
            # sql_database_array_xml[0] = data_xml_temp
        # if child.tag == "dewpoint_c":
            # data_xml_dewpoint = child.text
            # sql_database_array_xml[4] = data_xml_dewpoint
        # if child.tag == "wind_degrees":
            # data_xml_degrees = child.text 
            # sql_database_array_xml[2] = data_xml_degrees
        # if child.tag == "relative_humidity":
            # data_xml_humidity = child.text     
            # sql_database_array_xml[1] = data_xml_humidity
        # if child.tag == "windspeed_mph":
            # data_xml_windspeed = child.text 
            # sql_database_array_xml[5] = data_xml_windspeed
        # if child.tag == "pressure_mb":
            # data_xml_pressure = child.text
            # sql_database_array_xml[3] = data_xml_pressure
        # if child.tag == "observation_time_rfc822":
            # data_xml_time = child.text
    
    #todo: check to make sure no duplicate vals
    #pushToSQL()
    


def main():
    global rt
    # set up GUI window
    global window
    window.title("SQL Database Read-in")
    window.geometry('450x70')
    label_emptyRowCol_00 = Label(window,text="")
    label_emptyRowCol_00.grid(column=0,row=0)
    button_openFile = Button(window, text="Open Inverter Log Directory",command=openInverterLogDirButton)
    button_openFile.grid(column=1, row=1)
    button_openFile = Button(window, text="Open XML File",command=openXMLFileButton)
    button_openFile.grid(column=2, row=1)
    button_readFile = Button(window, text="Write to Database",command=startScriptButton)
    button_readFile.grid(column=3, row=1)
    button_forceStop = Button(window, text="Force Stop",command=forceStopButton)
    button_forceStop.grid(column=4, row=1)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # timer object
    rt = timer.RepeatedTimer(60, util.processFiles)
    
    window.mainloop() 
    
    

main()
