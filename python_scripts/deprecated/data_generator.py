# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 04:40:44 2019

@author: Lab
"""

#script to generate fake inverter data log file

from tkinter import Tk, Button, Label
import time
from threading import Timer
import random
import os

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

window = Tk()

time_hour = time.strftime("%H",time.localtime())
time_min  = time.strftime("%M",time.localtime())
time_sec  = time.strftime("%S",time.localtime())
time_year  = time.strftime("%Y",time.localtime())
time_month = time.strftime("%m",time.localtime())
time_day   = time.strftime("%d",time.localtime())

inverter_file = ""
inverter_file_name = time_year + "-" + time_month + "-" + time_day + ".log"
inverter_file_header = "[info]\nPlant Name: TestInverter\nDate:" + time_day + "/" + time_month + "/" + time_year + "\n\n"
inverter_file_measur = "[measurements]\nTime;Address;Model;MPPT;VDC1;IDC1;PDC1;VDC2;IDC2;PDC2;VAC;IAC;PAC;TINV;TINT;ENERGY;RISO;ILEAK;GENFREQ;\n;;;;VDC;ADC;W;VDC;ADC;W;V;A;W;°C;°C;Wh;MOhm;mA;Hz;\n\n"
inverter_file_start  = "[start]\n"
file_address_model_mppt = "2;PVI-4.2-OUTD-US-W;S;"
file_time = time_hour + ":" + time_min + ";"
file_vdc1 = str(round(random.uniform(0,0), 2)) + ";"
file_vdc2 = str(round(random.uniform(0,0), 2)) + ";"
file_idc1 = str(round(random.uniform(0,0), 2)) + ";"
file_idc2 = str(round(random.uniform(0,0), 2)) + ";"
file_pdc1 = str(round(random.uniform(0,0), 2)) + ";"
file_pdc2 = str(round(random.uniform(0,0), 2)) + ";"
file_vac  = str(round(random.uniform(0,0), 2)) + ";"
file_iac  = str(round(random.uniform(0,0), 2)) + ";"
file_pac  = str(round(random.uniform(0,0), 2)) + ";"
file_tinv = str(round(random.uniform(0,0), 2)) + ";"
file_tint = str(round(random.uniform(0,0), 2)) + ";"
file_energy  = str(round(random.uniform(0,0), 2)) + ";"
file_riso    = str(round(random.uniform(0,0), 2)) + ";"
file_ileak   = str(round(random.uniform(0,0), 2)) + ";"
file_genfreq = str(round(random.uniform(0,0), 2)) + ";"

xml_file = ""
xml_file_name = "weather_xml.xml"
file_time_stamp = ""
file_dewpoint_c = 0.0
file_pressure_mb = 0.0
file_relative_humidity = 0.0
file_temp_celsius = 0.0
file_wind_degrees = 0.0
file_windspeed_mph = 0.0
weather_xml_data = ""

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    def stop(self):
        self._timer.cancel()
        self.is_running = False

def generateRandom_data():
    global time_hour, time_minute, file_time
    global file_vdc1, file_vdc2, file_idc1, file_idc2, file_pdc1, file_pdc2 
    global file_vac, file_iac, file_pac 
    global file_tinv, file_tint, file_energy, file_riso, file_ileak, file_genfreq
    time_hour = time.strftime("%H",time.localtime())
    time_min  = time.strftime("%M",time.localtime())
    file_time = time_hour + ":" + time_sec + ";"
    file_vdc1 = str(round(random.uniform(50,80), 2)) + ";"
    file_idc1 = str(round(random.uniform(0,2), 2)) + ";"
    file_pdc1 = str(round(random.uniform(0,100), 2)) + ";"
    file_vdc2 = str(round(random.uniform(50,80), 2)) + ";"
    file_idc2 = str(round(random.uniform(0,2), 2)) + ";"
    file_pdc2 = str(round(random.uniform(0,100), 2)) + ";"
    file_vac  = str(round(random.uniform(190,220), 2)) + ";"
    file_iac  = str(round(random.uniform(0,2), 2)) + ";"
    file_pac  = str(round(random.uniform(300,500), 2)) + ";"
    file_tinv = str(round(random.uniform(20,30), 2)) + ";"
    file_tint = str(round(random.uniform(20,30), 2)) + ";"
    file_energy  = str(round(random.uniform(0,5), 2)) + ";"
    file_riso    = str(round(random.uniform(20,20), 2)) + ";"
    file_ileak   = str(round(random.uniform(100,210))) + ";"
    file_genfreq = str(round(random.uniform(0,60), 2)) + ";" 
    global file_time_stamp
    global file_dewpoint_c, file_pressure_mb, file_relative_humidity
    global file_temp_celsius, file_wind_degrees, file_windspeed_mph 
    file_time_stamp = time.strftime("%H:%M",time.localtime()) + ":" "00"
    file_dewpoint_c = str(round(random.uniform(0,30), 2))
    file_pressure_mb = str(round(random.uniform(500,2000), 2))
    file_relative_humidity = str(round(random.uniform(0,100), 2))
    file_temp_celsius = str(round(random.uniform(0,30), 2))
    file_wind_degrees = str(round(random.uniform(0,359), 2))
    file_windspeed_mph = str(round(random.uniform(0,30), 2))
    

def generateData():
    global rt
    global inverter_file, inverter_file_name
    global inverter_file_header, inverter_file_measur, inverter_file_start
    global xml_file, xml_file_name
    inverter_file = open(inverter_file_name,"a")
    inverter_file.write(inverter_file_header + inverter_file_measur + inverter_file_start)
    inverter_file.close()
    xml_file = open(xml_file_name,"a")
    xml_file.write("")
    xml_file.close()
    
    rt = RepeatedTimer(5, createFiles)
    rt.start()
    print("generate_clicked")

def prettify(elem):
    global weather_xml_data
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    weather_xml_data =  reparsed.toprettyxml(indent="  ")

def createXML():
    global file_time_stamp
    global file_dewpoint_c, file_pressure_mb, file_relative_humidity
    global file_temp_celsius, file_wind_degrees, file_windspeed_mph 
    top = Element('current_observation')
    child_dewpoint = SubElement(top, 'dewpoint_c')
    child_dewpoint.text = str(file_dewpoint_c)
    child_timestamp = SubElement(top, 'observation_time_rfc822')
    child_timestamp.text = str(file_time_stamp)
    child_pressure = SubElement(top, 'pressure_mb')
    child_pressure.text = str(file_pressure_mb)
    child_humidity = SubElement(top, 'relative_humidity')
    child_humidity.text = str(file_relative_humidity)
    child_temp = SubElement(top, 'temp_c')
    child_temp.text = str(file_temp_celsius)
    child_degrees = SubElement(top, 'wind_degrees')
    child_degrees.text = str(file_wind_degrees)
    child_speed = SubElement(top, 'windspeed_mph')
    child_speed.text = str(file_windspeed_mph)
    prettify(top) 


def createFiles():
    global inverter_file, xml_file
    inverter_file = open(inverter_file_name,"a")
    inverter_file.write(file_time + file_address_model_mppt + file_vdc1 + file_idc1 + file_pdc1 + file_vdc1 + file_idc1 + file_pdc2 + file_vac + file_iac + file_pac + file_tinv + file_tint + file_energy + file_riso + file_ileak + file_genfreq + "\n")
    inverter_file.close()
    
    createXML()
    if os.path.exists(xml_file_name):
        os.remove(xml_file_name)
    xml_file = open(xml_file_name,"a")
    xml_file.write(weather_xml_data)
    xml_file.close()
    
    generateRandom_data()
    
    print(time.strftime("%H:%M:%S",time.localtime()))
        
        
def forceStop():
    global rt
    rt.stop()    
    print("stopped_clicked")

def on_closing():  
    global window, inverter_file, xml_file
    inverter_file.close()
    xml_file.close()

    window.destroy()
    print("exited_window")

def main():
    global window
    window.title("Inverter Data Generator")
    window.geometry('300x70')
    label_emptyRowCol_00 = Label(window,text="")
    label_emptyRowCol_00.grid(column=0,row=0)
    label_emptyRowCol_21 = Label(window,text="")
    label_emptyRowCol_21.grid(column=2,row=1)
    button_generateData = Button(window, text="Generate Data",command=generateData )
    button_generateData.grid(column=1, row=1) 
    button_stopData = Button(window, text="Stop Data",command=forceStop)
    button_stopData.grid(column=3, row=1)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop() 
    
    
    
main()