import random

# Randomizes the distribution percentage of parcels across all districts
def randomizeParcelDist(nDistricts):
    parcelDist = [random.randint(1, 10)  for i in range(nDistricts)]
    parcelDist = [i/sum(parcelDist) for i in parcelDist]
    return parcelDist