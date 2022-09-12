'''
Alarm collector
stage 1
there is .txt file with site name
user can modify it
script takes sites from this file
and search for alarm in hisrory alarm
alarm name is fixed
open file(.csv) with history alarm
search for alarm which we are looking for
output result is whether alarm raised
if yes how many alarm was and for what sites
example output as below:
Alarm AAA raised N times at DD.MM.YYYY
site A   1 time 
site B   4 times

stage 2
take history alarm from 2 different files
search for special alarm
output how many alarms was per last 24hours

'''

#  Alarm Collector Stage 1 implementation
#  lets trace alarm "Board Value of Detecting Point Temperature(Celsius) threshold crossed(245)"

from datetime import date
from datetime import timedelta
import argparse

#alm_254 = "qazwsx fddfdf"  
#parser = argparse.ArgumentParser()
#parser.add_argument("alarm_name", default=alm_254, type=str, nargs='+')
#args = parser.parse_args()
root = 'historyAlarm'
  
alm_255 = "Board Value of Detecting Point Temperature(Celsius) threshold crossed(245)"
site_list_file = 'siteList.txt'

#print(' '.join(alm_255))

def site_lst(file):
    site_lst = []
    with open(file, 'r') as f:
        for line in f:
            site_lst.append(line.strip('\n'))
    return site_lst

def site_dict(site_list):
    site_dict = {}
    for site in site_list:
        site_dict.setdefault(site, 0)
    return site_dict    
        
site_dict = site_dict(site_lst(site_list_file)) 

def file_name_constr(today, root):    
    date = (str(today).split('-')[2] + str(today).split('-')[1])
    return root + '\\' + 'AlltheHistoryAlarms' + date + '.csv'

file_name = file_name_constr(date.today() - timedelta(days=1) , root)

def alm_search(file, alarm, site_dict):
    alm_count = 0
    with open(file, 'r') as f:        
        for line in f:
            if alarm in line:
                alm_count += 1                
            for site in site_dict:
                if site in line and alarm in line:
                    site_dict[site] += 1
        return alm_count, site_dict                           

total_alm_num, alm_dict = alm_search(file_name, alm_255, site_dict)                
date = date.today() - timedelta(days=1)
date_format = f'{date.day}.{date.month}.{date.year}'

def output(alm_name, alm_num, alm_dict, date_format):  #  we put result to file
    with open('result.txt', 'w', encoding='utf-8') as fl:
        if alm_num > 1:
            fl.write(f'Alarm "{alm_name}" raised {alm_num} times at {date_format}\n')
        else:
            fl.write(f'Alarm "{alm_name}" raised {alm_num} time at {date_format}\n')
    for site in alm_dict:
        if alm_dict[site] > 0:
            if alm_dict[site] > 1:
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{site:23} {alm_dict[site]} times\n')
            else:
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{site:23} {alm_dict[site]} time\n')                 

#output(alm_254, total_alm_num, alm_dict, date_format)

def main():
    if total_alm_num > 0:
        output(alm_255, total_alm_num, alm_dict, date_format)
        print('Collected success!')
        
if __name__ == '__main__':
    main()
