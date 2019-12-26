import mysql.connector
import re
import glob
import os
import datetime
import time
import urllib.request
import requests

index = 0
WeatherDataArrReversed = []
WeatherLatestXml = ""

thisYear  = time.strftime("%Y",time.localtime())
thisMonth = time.strftime("%m",time.localtime())
thisDay   = time.strftime("%d",time.localtime())

urlDate = thisYear + '-' + thisMonth + '-' + thisDay

# url = 'https://cuwx.clarkson.edu/xml/NoaaExt-' + urlDate + '.xml'
url = 'https://cuwx.clarkson.edu/json/NoaaExt-' + urlDate + '.json'
fullJsonData = urllib.request.urlopen(url).read().decode('utf-8')
# r = requests.get(url)
# fullXmlData = r.json()

# try:
#    os.remove('temp.txt')
# except OSError:
#     pass

# with open('temp.txt', 'w') as tempFile:
#     tempFile.write(fullXmlData)

# with open('temp.txt', 'r') as tempFile:
#     for line in reversed(list(tempFile)):
#         if(line == '<?xml version="1.0" encoding="UTF-8"?>\n'): 
#             WeatherDataArrReversed.append(line)
#             break
#         else:
#             WeatherDataArrReversed.append(line)
#         index = index + 1

# WeatherDataArrReversed = WeatherDataArrReversed[::-1]

# for i in range(len(WeatherDataArrReversed)):
#     WeatherLatestXml = WeatherLatestXml + WeatherDataArrReversed[i]

jsons = []
k = 0
length = len(fullJsonData)

for i in range(length-1):
    j = i+1
    if fullJsonData[i] == '}' and fullJsonData[j] == '{':
        jsons.append(fullJsonData[k:i])
        k = j

wxDate = re.search('(observation_time_rfc822":".*)(\d\d\s\w\w\w\s\d\d\d\d\s\d\d:\d\d:\d\d)', jsons[0]).group(2)
wxTemp = re.search('(temp_c":")(\d+.\d)', jsons[0]).group(2)
wxRelativeHumidity = re.search('(relative_humidity":")(\d+)', jsons[0]).group(2)
wxWindHeading = re.search('(wind_degrees":")(\d+)', jsons[0]).group(2)
wxPressure = re.search('(pressure_mb":")(\d+\.\d+)', jsons[0]).group(2)
wxDewpoint = re.search('(dewpoint_c":")(\d+\.\d+)', jsons[0]).group(2)
wxWindspeed = re.search('(wind_mph":")(\d+\.\d+)', jsons[0]).group(2)

# Original adds a minute for some reason
wxSecondString = wxDate[18:20]
wxSecondInteger = int(wxSecondString)
wxMinuteString = wxDate[15:17]    
wxMinuteInteger = int(wxMinuteString)
wxHourString = wxDate[12:14]
wxHourInteger = int(wxHourString)
wxDayString = wxDate[0:2]
wxDayInteger = int(wxDayString)
wxMonthString = wxDate[3:6]
wxYearString = wxDate[7:11]
wxYearInteger = int(wxYearString)
months = [['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
          [31,28,31,30,31,30,31,31,30,31,30,31]]
if wxSecondInteger >= 30: # Rounds up minute if past 30 seconds    
    if(wxMinuteInteger == 59):
        wxMinuteInteger = 00
        if wxHourInteger == 23:
            wxHourInteger == 00
            for i in range(12):
                if months[0][i] == wxMonthString:
                    break
            if wxYearInteger % 4 != 0:
                leapYear = False
            elif exYearInteger % 100 != 0:
                leapYear = True
            elif exYearInteger % 400 != 0:
                leapYear = False
            else:
                leapYear = True
    else:
        wxMinuteInteger = wxMinuteInteger + 1
    wxNewMinuteString = str(wxMinuteInteger)
    wxDate.replace(wxMinuteString,wxNewMinuteString)


wxConvertedTimestamp = datetime.datetime.strptime(wxDate, '%d %b %Y %H:%M:%S')

print(months)
print(months[1][3])
print(wxConvertedTimestamp)
