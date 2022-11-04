import random

# Generates the bonus efficiency granted to a driver depending on his affinity with the district
def bonusEfficiency(driver, district, base, nDistricts, nDrivers):
    normDriver, normDistrict = driver/nDrivers, district/nDistricts
    return round(base*(1 + abs(normDriver-normDistrict)*random.random()))