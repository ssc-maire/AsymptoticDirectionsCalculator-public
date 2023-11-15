import numpy as np
import pandas as pd
import datetime as dt
import shutil

try:
    assert not (shutil.which("magnetocosmics") is None)
except AssertionError:
    print("ERROR: AsympDirsCalculator currently requires magnetocosmics to be installed, such that the command 'magnetocosmics' can be run in terminal. All AsympDirsCalculator runs will currently fail until magnetocosmics is installed. If you have installed a copy of magnetocosmics, please check to see ensure that your paths have been set correctly, and that magneto-env.sh has been sourced correctly. If you are having issues or suspect there might be a bug, please feel free to report it at https://github.com/ssc-maire/AsymptoticDirectionsCalculator-public/issues , and I will try to respond to your issue as soon as I'm able to.")

from .MAGNETOCOSMICSrunManager import MAGNETOCOSMICSrunManager

def get_magcos_asymp_dirs(
                        array_of_lats_and_longs = np.array(np.meshgrid(np.linspace(-90.0,90.0,37), 
                                                np.linspace(0.0,355.0,72))).T.reshape(-1, 2),
                        array_of_zeniths_and_azimuths = np.array([[0.0, 0.0]]),
                        KpIndex=2,
                        dateAndTime=dt.datetime.now(), #dt.datetime(year=2010,month=6,day=1,hour=0,minute=0,second=0), 
                        highestMaxRigValue = 1010,
                        maxRigValue = 20,
                        minRigValue = 0.1,
                        nIncrements_high = 60,
                        nIncrements_low = 200,
                        cache=False,
                        full_output=False,
                        )->pd.DataFrame:

    print("running MAGNETOCOSMICS to acquire asymptotic directions...")
    MAGCOSrunManager = MAGNETOCOSMICSrunManager(dateAndTime, KpIndex, cache=cache)

    MAGCOSrunManager.set_rigidity_run_params(highestMaxRigValue,maxRigValue,minRigValue,nIncrements_high,nIncrements_low)
    MAGCOSrunManager.set_particle_direction_params(array_of_zeniths_and_azimuths)
    MAGCOSrunManager.run(array_of_lats_and_longs)
    dfOfAllAsymptoticDirections = MAGCOSrunManager.getOutputRigidities().sort_values(["initialLatitude","initialLongitude"])

    if full_output == False:
        dfOfAllAsymptoticDirections = dfOfAllAsymptoticDirections[["initialLatitude","initialLongitude","Rigidity","Lat","Long","Filter"]]

    return dfOfAllAsymptoticDirections

def get_magcos_vcutoffs(
                        array_of_lats_and_longs = np.array(np.meshgrid(np.linspace(-90.0,90.0,37), 
                                                np.linspace(0.0,355.0,72))).T.reshape(-1, 2),
                        array_of_zeniths_and_azimuths = np.array([[0.0, 0.0]]),
                        KpIndex=2,
                        dateAndTime=dt.datetime.now(), #dt.datetime(year=2010,month=6,day=1,hour=0,minute=0,second=0), 
                        highestMaxRigValue = 1010,
                        maxRigValue = 20,
                        minRigValue = 0.1,
                        nIncrements_high = 60,
                        nIncrements_low = 200,
                        cache=False,
                        )->pd.DataFrame:

    full_mag_cos_asymp_dir_DF = get_magcos_asymp_dirs(
                        array_of_lats_and_longs,
                        array_of_zeniths_and_azimuths,
                        KpIndex,
                        dateAndTime,
                        highestMaxRigValue,
                        maxRigValue,
                        minRigValue,
                        nIncrements_high,
                        nIncrements_low,
                        cache,
                        full_output=True,
                        )

    full_vcutoffs_DF = full_mag_cos_asymp_dir_DF.groupby(["initialLatitude","initialLongitude"]).last()[["Rlower","Reffective","Rupper"]]

    return full_vcutoffs_DF

