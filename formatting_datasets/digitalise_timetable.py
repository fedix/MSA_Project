"""
Transforms 'timetable' in KudaGo dataset (str):
'timetable': 'вт, чт 10:30–18:00, ср 10:30–21:00'
to the format of FIFA (ITMO) dataset:
dict of lists[int_1(opening time), int_2(closing time)]
'open_hours': {"1":[1030,1800],"4":[1030,1800], ...}
"""


import json
from json import JSONDecodeError
import re


# 1 - functions for digitalisation of KudaGo timetable 

# Convert time from 'str' to 'list[int_1, int_2]'
# Example: ('9:00-18:00') to [900, 1800]
def convert_time(text_time):
    
    time_range = re.split(r'[^\d:]', text_time[0])
    open_time = re.split(r'[^\d]', time_range[0])
    close_time = re.split(r'[^\d]', time_range[1])
    
    if open_time and close_time:
        time = [int(open_time[0] + open_time[1]),            int(close_time[0] + close_time[1])]
    else:
        time = None
    return time

def define_days(string):
    
    # Week days, example: "пн"
    mon = r'\bпн\b'
    tue = r'\bвт\b'
    wed = r'\bср\b'
    thu = r'\bчт\b'
    fri = r'\bпт\b'
    sat = r'\bсб\b'
    sun = r'\bвс\b'
    week = [mon, tue, wed, thu, fri, sat, sun]
    
    # Day range delimeter, example: "пн–ср"
    range_delimeter = r'–'
    
    # Other day defining notions:
    everyday = r'[Ее]жедневно'
    weekdays = r'[Бб]удни'
    
    work_days = []
    
    # if timetable provides range of days ("пн-ср"):
    day_range = re.search(range_delimeter, string)
    if day_range:
        start_day = 0
        end_day = 0
        for day in range(7):    # represents week days
            if(re.search(week[day] + range_delimeter,
                        string[0:day_range.end()])):
                start_day = day
            if(re.search(week[day],
                         string[day_range.end():])):
                end_day = day       
        for day in range(start_day, end_day+1):
            work_days.append(str(day))
            
    # Day enumeration ("пн, вт, ...""):
    for day in range(7):    # represents week days
        if(re.search(week[day], string)):
            work_days.append(str(day))
                
    # Everyday ("ежедневно"):
    if(re.search(everyday, string)):
        for day in range(7):
            work_days.append(str(day))
            
    # Weekdays ("по будним"):
    if(re.search(weekdays, string)):
        for day in range(5):
            work_days.append(str(day))
        
    return work_days

def digitalise(string):
    
    # Time range, example: "10:00-0:10"
    time_patt = r'\d{1,2}:\d\d[^,]\d{1,2}:\d\d'
    
    # Other time-notations:
    all_day = r'[Вв]есь день'
    always = r'[Кк]руглосуточно'
    last_visitor = r'[Дд]о последн'
    
    timetable = {}
    shift = 0
    
    # Work until last visitor case
    if re.search(last_visitor, string):
        # To allow time_range pattern below to work with this case
        # 'last_visitor' will be chaged to until '21:00' (assumption)
        string = re.sub(last_visitor, '21:00', string, count=0)
    
    # Standart time pattern case: 
    time = re.search(time_patt, string[shift:])
    while time:
        hours = convert_time(time)
        for day in define_days(string[shift:
                                      shift + time.start()]):
            if day not in timetable:
                timetable[day] = hours
        shift += time.end()
        time = re.search(time_patt, string[shift:])
        
    # All day open case:
    time = re.search(all_day, string)
    if time:
        hours = [0,0]
        for day in define_days(string[:time.start()]):
            if day not in timetable:
                timetable[day] = hours
    
    # Always open case:
    time = re.search(always, string)
    if time:
        timetable = {str(day):[0,0] for day in range(7)}
    return timetable

# 2 - output results:

if __name__ == "__main__":
    
    
    from collections import Counter
    
    
    # In / out files and directorires:
    direct = "D:/Work/Data_files/working_dir/"
    in_file_1 = "places_2_expand_spb"
    in_file_2 = "places_2_expand_msk"

    with open(direct + in_file_1 + ".json",
           'r', encoding = "utf-8") as inf_1, \
     open(direct + in_file_2 + ".json",
           'r', encoding = "utf-8") as inf_2:
        timetables = []
        count = Counter()
    
        try:
            places = json.load(inf_1)
            for place in places:
                timetable = place["timetable"]
                count[timetable] += 1
            places = json.load(inf_2)
            for place in places:
                timetable = place["timetable"]
                count[timetable] += 1
        except JSONDecodeError:
            print("Input file cannot be read")
    
        for word, count in count.most_common():
            print(word)
            print(digitalise(word))


