import time
import numpy as np
import datetime as dt

from AsympDirsCalculator.AsympDirsTools import get_magcos_asymp_dirs, get_magcos_vcutoffs

def test_simple_asymp_dir_run():

    outputtedAsympDirs = get_magcos_asymp_dirs(array_of_lats_and_longs = np.array([[0.0, 0.0],[1.0,1.0],[50.0,0.0]]))

    print(outputtedAsympDirs)

    pass

def test_simple_asymp_dir_run_verbose():

    outputtedAsympDirs = get_magcos_asymp_dirs(array_of_lats_and_longs = np.array([[0.0, 0.0],[1.0,1.0],[50.0,0.0]]), full_output=True)

    print(outputtedAsympDirs)

    pass

def test_simple_vcutoff_run():

    outputted_vcutoffs = get_magcos_vcutoffs(array_of_lats_and_longs = np.array([[0.0, 0.0],
                                                                                 [1.0,1.0],
                                                                                 [50.0,0.0]]))

    print(outputted_vcutoffs)

    pass

def test_simple_asymp_dir_run_cache():

    datetimeToUse = dt.datetime(year=2010, month=10, day=27)
    outputtedAsympDirs = get_magcos_asymp_dirs(array_of_lats_and_longs = np.array([[0.0, 0.0],[1.0,1.0]]),
                                               dateAndTime=datetimeToUse,
                                               cache=True)

    print(outputtedAsympDirs)

    pass

def test_full_world_run():

    start = time.time()
    get_magcos_asymp_dirs()
    end = time.time()
    print(end - start)
    
    with open("previousWorldRunTime.txt","w") as runTimeFile:
        runTimeFile.write(f"{end - start}")

def test_full_world_run_cache():

    datetimeToUse = dt.datetime(year=2010, month=10, day=27)

    start = time.time()
    asympDirList = get_magcos_asymp_dirs(KpIndex=6, dateAndTime=datetimeToUse, cache=True)
    end = time.time()
    print(end - start)