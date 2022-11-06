import os
import pandas as pd
import plotly
import plotly.express as px
import sys
import threading

sys.path.append(os.path.abspath('../functions'))
from functions.optimizeWithUncertainty import optimizeWithUncertainty

def optimizeUncertaintyTests(type, vars):
    """
    Runs tests for optimisation over a given time period with a chance for parcels to be returned.
    """
    
    if (type == 'varyReturnRate'):
        profitsUncertaintyVaryReturnRate = {
            'name' : [],
            'day' : [],
            'profit' : []
        }
        
        for var in vars:
            currCat = str(var) + ' Return Rate'
            t = threading.Thread(target=optimizeWithUncertainty, 
                                                args=(
                                                    profitsUncertaintyVaryReturnRate, # dataDict
                                                    currCat, # cat
                                                    var, # returnRate
                                                    7, # nDays
                                                    5, # nDistricts
                                                    20, # nDrivers
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
            
        df = pd.DataFrame(profitsUncertaintyVaryReturnRate)
        fig = px.line(df, x='day', y='profit', color='name')
        plotly.offline.plot(fig,filename='profitsUncertaintyVaryReturnRate.html',config={'displayModeBar': False})