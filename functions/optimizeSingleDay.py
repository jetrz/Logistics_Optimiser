from .bonusEfficiency import bonusEfficiency
from .randomizeParcelDist import randomizeParcelDist

import numpy as np
import random
from rsome import ro
from rsome import grb_solver as grb

def optimizeSingleDay(dataDict, cat, iteration, nDistricts, nDrivers, totalParcels, costDelivered, costUndelivered, costDriver, maxHours, minDriverEfficiency, maxDriverEfficiency):
    """
    Optimizes capacity planning for a single day.

    Args:
        dataDict (object): Data object to store return values
        cat (string): Category of current call
        iteration (int): Iteration of current call
        nDistricts (int): Number of districts to deliver to
        nDrivers (int): Number of drivers available
        totalParcels (int): Total number of parcels to deliver
        costDelivered (int): Amount earned per successful delivery
        costUndelivered (int): Cost per undelivered parcel
        costDriver (int): Hourly wage of each driver
        maxHours (int): Maximum number of hours each driver can work
        minDriverEfficiency (int): Lower bound of the efficiency of each driver (in terms of parcels per hour)
        maxDriverEfficiency (int): Upper bound of the efficiency of each driver (in terms of parcels per hour)
    """
    
    # Static variables
    model = ro.Model()
    parcelDist = randomizeParcelDist(nDistricts)
    parcels = [round(i*totalParcels) for i in parcelDist]
    parcels[-1] = totalParcels - sum(parcels[:-1])
    
    baseEfficiency = [random.randint(minDriverEfficiency, maxDriverEfficiency) for i in range(nDrivers)]
    efficiencyMatrix = np.array([[bonusEfficiency(i, j, baseEfficiency[i], nDistricts, nDrivers) for i in range(nDrivers)] for j in range(nDistricts)])
    
    # Decision variables
    deliveringAmt = model.dvar((nDistricts, nDrivers), 'I') # 2D Matrix to keep track of the number of parcels each driver is delivering for each district
    deliveringHours = model.dvar((nDistricts, nDrivers), 'C') # 2D Matrix to keep track of the number of hours each driver is putting in for each district
    isDelivering = model.dvar((nDistricts, nDrivers), 'B') # 2D Matrix to keep track if a driver is delivering to a district
    
    # Objective
    model.max(deliveringAmt.sum()*costDelivered - (totalParcels - deliveringAmt.sum())*costUndelivered - deliveringHours.sum()*costDriver)

    # Constraints
    # Each driver cannot deliver more than his efficiency x hours
    for i in range(nDistricts):
        for j in range(nDrivers):
            model.st(0 <= deliveringAmt[i][j], deliveringAmt[i][j] <= efficiencyMatrix[i][j]*deliveringHours[i][j])
            
    # Each driver cannot drive more hours than the max allowed
    for i in range(nDistricts):
        for j in range(nDrivers):
            model.st(0 <= deliveringHours[i][j], deliveringHours[i][j] <= isDelivering[i][j]*maxHours)
        
    # Each driver can only deliver to 1 district
    model.st(isDelivering.sum(axis=0) <= 1)

    # Number of parcels delivered per region cannot exceed total number of parcels available to be delivered to that region
    model.st(deliveringAmt[i].sum() <= parcels[i] for i in range(nDistricts))

    model.solve(solver=grb)
    # print('deliveringAmt: ', deliveringAmt.get())
    # print('deliveringHours: ', deliveringHours.get())
    dataDict['name'].append(cat)
    dataDict['iteration'].append(iteration)
    dataDict['profit'].append(model.get())
    return 1