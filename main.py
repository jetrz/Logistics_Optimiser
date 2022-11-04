from tests.optimizeSingleTests import optimizeSingleTests
from tests.optimizePeriodTests import optimizePeriodTests

if __name__ == "__main__":
    # First, we perform analysis for single day optimisation.
    # Varying number of drivers:
    # optimizeSingleTests(type='varyDriver', vars=[5,15,25,35,45,55], iters=30)
    # Varying number of districts:
    # optimizeSingleTests(type='varyDistrict', vars=[1,5,15,25,35,45], iters=30)
    
    # In reality, parcels not delivered at the end of the day are left to the next day.
    # Now, we introduce the dimension of time.
    optimizePeriodTests(type='varyDriver', vars=[1,5,10,15,20], nDays=14)
        