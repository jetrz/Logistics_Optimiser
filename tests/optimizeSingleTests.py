import os
import pandas as pd
import plotly
import plotly.express as px
import sys
import threading

sys.path.append(os.path.abspath('../functions'))
from functions.optimizeSingleDay import optimizeSingleDay


def optimizeSingleTests(type, vars, iters):
    """
    Runs tests for single day optimisation.
    """
    
    if (type == 'varyDriver'):
        profitsSingleDayVaryDrivers = {
            'name' : [],
            'iteration' : [],
            'profit' : []
        }
        
        for i in range(iters):
            for j in range(len(vars)):
                currCat = str(vars[j]) + ' Drivers'
                t = threading.Thread(target=optimizeSingleDay, 
                                                    args=(
                                                        profitsSingleDayVaryDrivers, # dataDict
                                                        currCat, # cat
                                                        i, # iteration
                                                        28, # nDistricts
                                                        vars[j], # nDrivers
                                                        1300, # Total Parcels
                                                        10, # costDelivered
                                                        8, # costUndelivered
                                                        20, # costDriver
                                                        8, # maxHours
                                                        3, # minDriverEfficiency
                                                        10, # maxDriverEfficiency
                                                    ))
                t.start()
                t.join(timeout=300)
            
        df = pd.DataFrame(profitsSingleDayVaryDrivers)
        fig = px.line(df, x='iteration', y='profit', color='name')
        plotly.offline.plot(fig,filename='profitsSingleDayVaryDrivers.html',config={'displayModeBar': False})
    elif (type == 'varyDistrict'):
        profitsSingleDayVaryDistricts = {
            'name' : [],
            'iteration' : [],
            'profit' : []
        }
        
        for i in range(iters):
            for j in range(len(vars)):
                currCat = str(vars[j]) + ' Districts'
                t = threading.Thread(target=optimizeSingleDay, 
                                                    args=(
                                                        profitsSingleDayVaryDistricts, # dataDict
                                                        currCat, # cat
                                                        i, # iteration
                                                        vars[j], # nDistricts
                                                        45, # nDrivers
                                                        1300, # Total Parcels
                                                        10, # costDelivered
                                                        8, # costUndelivered
                                                        20, # costDriver
                                                        8, # maxHours
                                                        3, # minDriverEfficiency
                                                        10, # maxDriverEfficiency
                                                    ))
                t.start()
                t.join(timeout=300)
            
        df = pd.DataFrame(profitsSingleDayVaryDistricts)
        fig = px.line(df, x='iteration', y='profit', color='name')
        plotly.offline.plot(fig,filename='profitsSingleDayVaryDistricts.html',config={'displayModeBar': False})