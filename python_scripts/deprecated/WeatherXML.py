# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 16:48:22 2019

@author: Chris Mark, Ryan Wood
"""

#this would take the URL and create a file from it

import urllib
import os
import re
import time
import datetime


index = 0
WeatherDataArrReversed = []
Weather_array = []
WeatherLatestXml = ""
new_Var = ""

thisYear  = time.strftime("%Y",time.localtime())
thisMonth = time.strftime("%m",time.localtime())
thisDay   = time.strftime("%d",time.localtime())

urlDate = thisYear + '-' + thisMonth + '-' + thisDay

url = 'https://cuwx.clarkson.edu/xml/NoaaExt-' + urlDate + '.xml'
fullXmlData = urllib.request.urlopen(url).read().decode('utf-8')

try:
    os.remove('temp.txt')
except OSError:
    pass

try:
    os.remove('latestWeatherXML.xml')
except OSError:
    pass

with open('temp.txt', 'w') as tempFile:
    tempFile.write(fullXmlData)

with open('temp.txt', 'r') as tempFile:
    for line in reversed(list(tempFile)):
        if(line == '<?xml version="1.0" encoding="UTF-8"?>\n'): 
            WeatherDataArrReversed.append(line)
            break
        else:
            WeatherDataArrReversed.append(line)
        index = index + 1

WeatherDataArrReversed = WeatherDataArrReversed[::-1]

for i in range(len(WeatherDataArrReversed)):
    WeatherLatestXml = WeatherLatestXml + WeatherDataArrReversed[i]


wxDate = re.search('(?:<observation_time>Last Updated on )(.*)(?: EDT</observation_time>)', WeatherLatestXml).group(1)
wxTemp = re.search('(?:<temp_c>)(.*)(?:</temp_c>)', WeatherLatestXml).group(1)
wxRelativeHumidity = re.search('(?:<relative_humidity>)(.*)(?:</relative_humidity>)', WeatherLatestXml).group(1)
wxWindHeading = re.search('(?:<wind_degrees>)(.*)(?:</wind_degrees>)', WeatherLatestXml).group(1)
wxPressure = re.search('(?:<pressure_mb>)(.*)(?:</pressure_mb>)', WeatherLatestXml).group(1)
wxDewpoint = re.search('(?:<dewpoint_c>)(.*)(?:</dewpoint_c>)', WeatherLatestXml).group(1)
wxWindSpeed = re.search('(?:<wind_mph>)(.*)(?:</wind_mph>)', WeatherLatestXml).group(1)


wxConvertedTimestamp = datetime.datetime.strptime(wxDate, '%b %d %Y, %H:%M %p')

print('Timestamp: ' + wxDate)
print('Temperature(c): ' + wxTemp)
print('Relative humidity: ' + wxRelativeHumidity)
print('Wind heading: ' + wxWindHeading)
print('Pressure (mb): ' + wxPressure)
print('Dewpoint: ' + wxDewpoint)
print('Windspeed: ' + wxWindSpeed)

return wxConvertedTimestamp, wxTemp, wxRelativeHumidity, wxWindHeading, wxPressure, wxDewpoint, wxWindspeed

#print(m.group(1))


#
#Weather_file = open('WeatherXML2.xml', 'w')
#Weather_file.write(Weather_xml)
#Weather_file.close()
#
##create a URL request for the xml and convert to a file
##response = requests.get(URL)
##with open('feed.xml', 'wb') as file:
##    file.write(response.content)
#
##Parse the file    
#tree = ET.parse('WeatherXML2.xml')
#root = tree.getroot()
#
##convert the tag (name) and text (data) 
#
#for child in root:
#    if child.tag == "temp_c":
#        temp_celsius_xml = child.text        
#        print(child.tag + ":" + child.text + ":" + "\n")    
#    if child.tag == "dewpoint_c":
#        dewpoint_celsius_xml = child.text
#        print(child.tag + ":" + child.text + ":" + "\n")    
#    if child.tag == "wind_degrees":
#        wind_heading_xml = child.text        
#        print(child.tag + ":" + child.text + ":" + "\n")   
#    if child.tag == "relative_humidity":
#        relative_humidity_xml = child.text        
#        print(child.tag + ":" + child.text + ":" + "\n")
#    if child.tag == "wind_mph":
#        windspeed_mph_xml = child.text        
#        print(child.tag + ":" + child.text + ":" + "\n") 
#    if child.tag == "pressure_mb":
#        pressure_mb_xml = child.text
#        print(child.tag + ":" + child.text + ":" + "\n")
#
#
#
#    
