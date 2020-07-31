# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 23:13:01 2020

@author: Arjan
"""

import pandas as pd
from datetime import date
from pushtocal import push_event

data = pd.read_csv('./waterstanden.csv', delimiter=';', index_col=False)

for index in data.index:
    data['Meting'][index] = float(data['Meting'][index][1:-3])
    
today = date.today().strftime('%d/%m/%Y')

data_today = (data[data['Datum'] == today].sort_values(by='Tijd'))
agenda_string = ""

for index in data_today.index:
    tijd = data_today.loc[index, 'Tijd']
    HWLW = data_today.loc[index, 'Hoogwater/laagwater']
    if 'H' in HWLW:
        HWLW = 'hoog'
    else:
        HWLW = 'laag'
    stand = data_today.loc[index, 'Meting']
    
    if agenda_string:
        agenda_string = (f"{agenda_string}\n{tijd}, {HWLW}water {stand} cm")
    else:
        agenda_string = (f"{tijd}, {HWLW}water {stand} cm")
        
event = {
    'summary': f"Waterstand {today}",
    'description': agenda_string,
    'start': {
        'date': date.today().strftime('%Y-%m-%d')
        },
    'end': {
        'date': date.today().strftime('%Y-%m-%d')
        }
    }

if date.today().isoweekday() == 6:
    response = push_event(event)
    print(response)
    
