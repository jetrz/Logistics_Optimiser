from .bonusEfficiency import bonusEfficiency
from .randomizeParcelDist import randomizeParcelDist

import numpy as np
import random
from rsome import ro
from rsome import grb_solver as grb

def optimizeOverPeriod(dataDict, cat, nDays, nDistricts, nDrivers, totalParcelsAvg, totalParcelsSD, costDelivered, costUndelivered, costDriver, maxHours, minDriverEfficiency, maxDriverEfficiency):
    """
    Optimizes capacity planning over a period of time.

    Args:
        dataDict (object): Data object to store return values
        cat (string): Category of current call
        nDays (int): Number of days to run optimizer over
        nDistricts (int): Number of districts to deliver to
        nDrivers (int): Number of drivers available
        totalParcelsAvg (int): Average number of parcels to deliver each day
        totalParcelsSD (int): Standard deviation of the number of parcels to deliver each day
        costDelivered (int): Amount earned per successful delivery
        costUndelivered (int): Cost per undelivered parcel at the end of every day
        costDriver (int): Hourly wage of each driver
        maxHours (int): Maximum number of hours each driver can work each day
        minDriverEfficiency (int): Lower bound of the efficiency of each driver (in terms of parcels per hour)
        maxDriverEfficiency (int): Upper bound of the efficiency of each driver (in terms of parcels per hour)
    """
    # Static Variables
    # Randomize the base number of parcels to be delivered each day
    baseParcels = [round(np.random.normal(totalParcelsAvg,totalParcelsSD)) for i in range(nDays)]
    parcelDist = randomizeParcelDist(nDistricts)
    
    baseEfficiency = [random.randint(minDriverEfficiency, maxDriverEfficiency) for i in range(nDrivers)]
    efficiencyMatrix = np.array([[bonusEfficiency(i, j, baseEfficiency[i], nDistricts, nDrivers) for i in range(nDrivers)] for j in range(nDistricts)])
    efficiencyMatrix = np.tile(efficiencyMatrix, [nDays,1,1])
    
    model = ro.Model()

    # Decision Variables
    deliveringAmt = model.dvar((nDays, nDistricts, nDrivers), 'C') # 3D Matrix to keep track of the number of parcels each driver is delivering to each district each day
    deliveringHours = model.dvar((nDays, nDistricts, nDrivers), 'C') # 3D Matrix to keep track of the number of hours each driver is putting in for each district each day
    isDelivering = model.dvar((nDays, nDistricts, nDrivers), 'B') # 3D Matrix to keep track if a driver is delivering to a district each day
    undeliveredParcels = model.dvar(nDays, 'C') # List to track the number of undelivered parcels each day
    profits = model.dvar(nDays, 'C') # Keeps track of the profits of each day
    
    # Objective
    model.max(profits.sum())

    # Constraints
    # Daily profit depends on number of parcels succesfully delivered and number of hours worked across all drivers
    model.st(profits[i] <= deliveringAmt[i].sum()*costDelivered - undeliveredParcels[i]*costUndelivered - deliveringHours[i].sum()*costDriver for i in range(nDays))
    
    # Parcels to be delivered each day is calculated with that day's base + ytd leftover
    model.st(undeliveredParcels[0] >= baseParcels[0]-deliveringAmt[0].sum())
    model.st(undeliveredParcels[i] >= baseParcels[i]+undeliveredParcels[i-1]-deliveringAmt[i].sum() for i in range(1, nDays))

    # Each driver cannot deliver more than his efficiency*hours
    # for i in range(nDays):
    #     for j in range(nDistricts):
    #         for k in range(nDrivers):
    #             model.st(0 <= deliveringAmt[i][j][k], deliveringAmt[i][j][k] <= efficiencyMatrix[i][j][k]*deliveringHours[i][j][k])
    model.st(0 <= deliveringAmt, deliveringAmt <= efficiencyMatrix*deliveringHours)
    # model.st(0 <= deliveringAmt, deliveringAmt <= deliveringHours)
            
    # Each driver cannot drive more hours than the max allowed
    # for i in range(nDays):
    #     for j in range(nDistricts):
    #         for k in range(nDrivers):
    #             model.st(0 <= deliveringHours[i][j][k], deliveringHours[i][j][k] <= isDelivering[i][j][k]*maxHours)
    model.st(0 <= deliveringHours, deliveringHours <= isDelivering*maxHours)
        
    # Each driver can only deliver to 1 district
    model.st(isDelivering[i].sum(axis=0) <= 1 for i in range(nDays))

    # Number of parcels delivered per region cannot exceed total number of parcels available to be delivered to that region
    for i in range(nDays):
        for j in range(nDistricts):
            if (i == 0):
                model.st(deliveringAmt[i][j].sum() <= baseParcels[i]*parcelDist[j])
            else:
                model.st(deliveringAmt[i][j].sum() <= (baseParcels[i]+undeliveredParcels[i-1])*parcelDist[j])

    model.solve(solver=grb, params={'LogToConsole': 0})
    print(isDelivering.get())
    resProfits = profits.get()
    for i in range(len(resProfits)):
        dataDict['name'].append(cat)
        dataDict['day'].append(i+1)
        dataDict['profit'].append(resProfits[i])
    return 1
