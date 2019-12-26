# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:09:42 2019

@author: ryans


    


"""

import mysql.connector
import re
import glob
import os
import datetime
import time
import urllib.request
#import requests

DB_ADDRESS = "128.153.21.86"
DB_USERNAME = "pythondev"
DB_PASSWORD = "WMDccp2018!"
DB_NAME = "blackboard_gui"

firstRunFlag = 1

timestamp = None
vdc1 = None
idc1 = None
pdc1 = None
vdc2 =  None
idc2 =  None
pdc2 =  None
vac  =  None
iac  =  None
pac  =  None
tinv =  None
tint =  None
energy = None
riso   = None
ileak  = None
freq = None
temp = None
humidity = None
degrees = None
pressure = None
dewpoint = None
speed = None

inverterDateString = ""
inverterDataString = ""

inverterDataArr = [timestamp, vdc1, idc1, pdc1, vdc2, idc2, pdc2, vac, iac, pac, tinv, tint, energy, riso, ileak, freq]
weatherDataArr = [temp, humidity, degrees, pressure, dewpoint, speed]

inverterLogDirPath = ''
weatherXmlPath = ''
inverterLogFilePath = ''

# chooses the most recently edited file from the specified directory
def chooseInverterLogFile():
    global inverterLogDirPath, inverterLogFilePath
    fileList = glob.glob(inverterLogDirPath + '/*.log')
    inverterLogFilePath = max(fileList, key=os.path.getctime)
    print('Most recently edited file: ' + inverterLogFilePath)

def processFiles():
    global firstRunFlag
    # read inverter log
    chooseInverterLogFile()
    inverterDateLine, inverterDataString, timestampErrorFlag = readInverterLogFile();

    # read current weather data
    #wxTimestamp, wxTemp, wxRelativeHumidity, wxWindHeading, wxPressure, wxDewpoint, wxWindspeed = getWeatherData()
    weatherData = getWeatherData()

    inverterTimestamp = datetime.datetime.strptime(inverterDataString[:5], '%H:%M').replace(day=int(inverterDateLine[6:8], 10), 
             month=int(inverterDateLine[9:11], 10), year=int(inverterDateLine[12:16], 10))
    print('Inverter timestamp:')
    print(inverterTimestamp)

    print('Wx timestamp:')
    print(weatherData[0])
    
    if(inverterTimestamp != weatherData[0]):
        print('Nonmatching dates!')
        #pushNormalSampleToSQL(inverterDateLine, inverterDataString, [None, None, None, None, None, None, None])
    # sql insert into database
    if timestampErrorFlag == 1:
            if firstRunFlag == 0:
                print('WARNING: Duplicate timestamp. Is the inverter off?')
    else:
        pushNormalSampleToSQL(inverterDateLine, inverterDataString, weatherData)
        print('pushing')
        print(inverterDateLine)
        print(weatherData[0])
        print("Weather Data: ")
        print(weatherData)
        pass
    # end with setting values to null to prevent repeat data
    setAttribsNull()

def readInverterLogFile():
    global inverterLogFilePath
    inverter_file = open(inverterLogFilePath, 'r')
    lines = inverter_file.read().splitlines()
    
    inverterDateString = lines[2].rstrip()

    dbLastTimestamp = getMostRecentSqlTimestamp()
    
    for line in lines:
        if re.match('^\d\d:\d\d', line):
            logTimestamp = datetime.datetime.strptime(line[:5], '%H:%M').replace(day=int(inverterDateString[6:8], 10), 
                                 month=int(inverterDateString[9:11], 10), year=int(inverterDateString[12:16], 10))
            if (dbLastTimestamp is not None):
                    inverterDataString = line
    inverter_file.close()
    
    if dbLastTimestamp != logTimestamp:
        duplicateTimestampFlag = 0
    else:
        duplicateTimestampFlag = 1
        
    return inverterDateString, inverterDataString, duplicateTimestampFlag

def getMissedInverterData():
    global inverterLogFilePath
    print('Gathering missed data')
    dbLastTimestamp = getMostRecentSqlTimestamp()
    inverter_file = open(inverterLogFilePath, 'r')
    lines = inverter_file.read().splitlines()
        
    inverterDateString = lines[2].rstrip()
    count = 0
    if (dbLastTimestamp is not None):
        print('Most recent timestamp in DB: ' + dbLastTimestamp.strftime('%Y-%m-%d %H:%M'))
    
        dbLastTimestampHourMin = datetime.datetime.strptime(dbLastTimestamp.strftime('%H:%M'),'%H:%M')


        for line in lines:
            if re.match('^\d\d:\d\d', line):
                logTimeStamp = datetime.datetime.strptime(line[:5], '%H:%M')
                if logTimeStamp > dbLastTimestampHourMin:
                    dbLastTimestampHourMin = logTimeStamp
                    # line needs to be pushed to db
                    pushNormalSampleToSQL(inverterDateString, line,[None, None, None, None, None, None, None])
                    count += 1
    else:
        for line in lines:
            if re.match('^\d\d:\d\d', line):
                # line needs to be pushed to db
                pushNormalSampleToSQL(inverterDateString, line, [None, None, None, None, None, None, None])
                count += 1
            
            
    inverter_file.close()
    
    print(str(count) + ' missed data lines added to database')
    
def getWeatherData():   
    index = 0
    WeatherDataArrReversed = []
    WeatherLatestXml = ""
    
    thisYear  = time.strftime("%Y",time.localtime())
    thisMonth = time.strftime("%m",time.localtime())
    thisDay   = time.strftime("%d",time.localtime())
    
    urlDate = thisYear + '-' + thisMonth + '-' + thisDay
    
    url = 'https://cuwx.clarkson.edu/xml/NoaaExt-' + urlDate + '.xml'
    # url = 'https://cuwx.clarkson.edu/json/NoaaExt-' + urlDate + '.json'
    fullXmlData = urllib.request.urlopen(url).read().decode('utf-8')
    # r = requests.get(url)
    # fullXmlData = r.json()
    
    try:
        os.remove('temp.txt')
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
    
    wxDate = re.search('(?:<observation_time_rfc822>.*[,] )(.*)(?:[:][0-9][0-9] [-+].*</observation_time_rfc822>)', WeatherLatestXml).group(1)
    wxTemp = re.search('(?:<temp_c>)(.*)(?:</temp_c>)', WeatherLatestXml).group(1)
    wxRelativeHumidity = re.search('(?:<relative_humidity>)(.*)(?:</relative_humidity>)', WeatherLatestXml).group(1)
    wxWindHeading = re.search('(?:<wind_degrees>)(.*)(?:</wind_degrees>)', WeatherLatestXml).group(1)
    wxPressure = re.search('(?:<pressure_mb>)(.*)(?:</pressure_mb>)', WeatherLatestXml).group(1)
    wxDewpoint = re.search('(?:<dewpoint_c>)(.*)(?:</dewpoint_c>)', WeatherLatestXml).group(1)
    wxWindspeed = re.search('(?:<wind_mph>)(.*)(?:</wind_mph>)', WeatherLatestXml).group(1)
    
    wxMinuteString = wxDate[15:17]    
    wxMinuteInteger = int(wxMinuteString)
    if(wxMinuteInteger == 59):
        wxMinuteInteger == 00
    else:
        wxMinuteInteger = wxMinuteInteger + 1
    wxNewMinuteString = str(wxMinuteInteger)
    wxDate.replace(wxMinuteString,wxNewMinuteString)
    
    
    
    wxConvertedTimestamp = datetime.datetime.strptime(wxDate, '%d %b %Y %H:%M')
    
    print(wxConvertedTimestamp)
    return [wxConvertedTimestamp, wxTemp, wxRelativeHumidity, wxWindHeading, wxPressure, wxDewpoint, wxWindspeed]

    
def getMostRecentSqlTimestamp():
    mydb = mysql.connector.connect(host=DB_ADDRESS, user=DB_USERNAME, passwd=DB_PASSWORD, database=DB_NAME)
    mycursor = mydb.cursor()
    sql = ("SELECT MAX(time_stamp) FROM inverter_and_weather_data")
    mycursor.execute(sql)
    result = mycursor.fetchone()
    mycursor.close()
    mydb.close()

    return result[0]

    
def pushNormalSampleToSQL(inverterDateString, inverterDataString, wxDataArr):
    global inverterDataArr
    inverterDataString = inverterDataString.replace("2;PVI-4.2-OUTD-US-W;S;","",1)

    # set up value strings for database insertion
    for t in range(len(inverterDataArr)):
        if t == 0:
            inverterDateString = str(inverterDateString.rsplit(':')[1]).replace("\n","") + " " + (inverterDataString.rsplit(';', -1)[t]) + ":00"
            inverterDateString = inverterDateString[7:11] + "-" + inverterDateString[4:6] + "-" + inverterDateString[1:3] + inverterDateString[11:20]
            inverterDataArr[t] = inverterDateString
        else:
            inverterDataArr[t] = (inverterDataString.rsplit(';', -1)[t])    
    
    mydb = mysql.connector.connect(host=DB_ADDRESS, user="pythondev", passwd="WMDccp2018!", database="blackboard_gui")
    mycursor = mydb.cursor()
    sql = ("INSERT INTO inverter_and_weather_data (time_stamp, VDC1, IDC1, PDC1, VDC2, IDC2, PDC2, VAC, IAC, PAC, TINV, TINT, ENERGY, RISO, ILEAK, GENFREQ, temp_celsius, relative_humidity, wind_heading, pressure_mb, dewpoint_celsius, windspeed_mph) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = inverterDataArr + wxDataArr[1:]
    
    mycursor.execute(sql, data)
    mydb.commit()
    mycursor.close()
    mydb.close()
    
    
def setAttribsNull():
    global inverterDataArr, weatherDataArr
    for inverterArr, wxArr in zip(inverterDataArr, weatherDataArr):
        inverterArr = None
        wxArr = None
