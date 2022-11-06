import os
import pandas as pd
import plotly
import plotly.express as px
import sys
import threading

sys.path.append(os.path.abspath('../functions'))
from functions.optimizeOverPeriod import optimizeOverPeriod

def optimizePeriodTests(type, vars, nDays):
    """
    Runs tests for optimisation over a given time period.
    """
    
    if (type == 'varyDriver'):
        profitsTimePeriodVaryDrivers = {
            'name' : [],
            'day' : [],
            'profit' : []
        }
        
        for var in vars:
            currCat = str(var) + ' Drivers'
            t = threading.Thread(target=optimizeOverPeriod, 
                                                args=(
                                                    profitsTimePeriodVaryDrivers, # dataDict
                                                    currCat, # cat
                                                    nDays, # nDays
                                                    5, # nDistricts
                                                    var, # nDrivers
                                                    1300, # totalParcelsAvg
                                                    200, # totalParcelsSD
                                                    10, # costDelivered
                                                    8, # costUndelivered
                                                    20, # costDriver
                                                    8, # maxHours
                                                    3, # minDriverEfficiency
                                                    10, # maxDriverEfficiency
                                                ))
            t.start()
            t.join(timeout=300)
            
        df = pd.DataFrame(profitsTimePeriodVaryDrivers)
        fig = px.line(df, x='day', y='profit', color='name')
        plotly.offline.plot(fig,filename='profitsTimePeriodVaryDrivers.html',config={'displayModeBar': False})
    elif (type == 'varyDistrict'):
        profitsTimePeriodVaryDistricts = {
            'name' : [],
            'day' : [],
            'profit' : []
        }
        
        for var in vars:
            currCat = str(var) + ' Districts'
            t = threading.Thread(target=optimizeOverPeriod, 
                                                args=(
                                                    profitsTimePeriodVaryDistricts, # dataDict
                                                    currCat, # cat
                                                    nDays, # nDays
                                                    var, # nDistricts
                                                    10, # nDrivers
                                                    650, # totalParcelsAvg
                                                    65, # totalParcelsSD
                                                    10, # costDelivered
                                                    8, # costUndelivered
                                                    20, # costDriver
                                                    8, # maxHours
                                                    3, # minDriverEfficiency
                                                    10, # maxDriverEfficiency
                                                ))
            t.start()
            t.join(timeout=300)
            
        df = pd.DataFrame(profitsTimePeriodVaryDistricts)
        fig = px.line(df, x='day', y='profit', color='name')
        plotly.offline.plot(fig,filename='profitsTimePeriodVaryDistricts.html',config={'displayModeBar': False})