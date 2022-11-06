from tests.optimizeSingleTests import optimizeSingleTests
from tests.optimizePeriodTests import optimizePeriodTests
from tests.optimizeUncertaintyTests import optimizeUncertaintyTests

if __name__ == "__main__":
    """
    Runs analysis for the various models. Please uncomment the appropriate lines to test.
    Please view the respective tests files to understand the syntax as well.
    """
    # First, we perform analysis for single day optimisation.
    # Varying number of drivers:
    # optimizeSingleTests(type='varyDriver', vars=[5,15,25,35,45,55], iters=30)
    # Varying number of districts:
    # optimizeSingleTests(type='varyDistrict', vars=[1,5,15,25,35,45], iters=30)
    # Varying upper limit of driver efficiency:
    # optimizeSingleTests(type='varyDriverEfficiencyUpperLimit', vars=[5,10,15,20,25,30], iters=30)
    
    # In reality, parcels not delivered at the end of the day are left to the next day.
    # Now, we introduce the dimension of time.
    # Varying number of drivers:
    # optimizePeriodTests(type='varyDriver', vars=[5,10,15,25,30], nDays=14)
    # Varying number of districts:
    # optimizePeriodTests(type='varyDistrict', vars=[2,4,6,8,10,12,15], nDays=5)
        
    # Finally, we want to add an element of uncertainty, as there is a chance that a parcel is returned.
    # optimizeUncertaintyTests(type='varyReturnRate', vars=[0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 0.9])