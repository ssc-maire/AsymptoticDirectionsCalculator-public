#!/bin/python3

import datetime as dt
import numpy as np
import pandas as pd

from .MAGNETOCOSMICSrun import MAGNETOCOSMICSrun, get_magcos_cache_function


class MAGNETOCOSMICSrunManager():

    _runMode = "General"

    def __init__(self, 
                 dateAndTime:dt.datetime,
                 KpIndex:int,
                 cache=False,
                 ):

        self._date_and_time = dateAndTime
        self._kp_index = KpIndex
        self.set_MAGCOS_run_function(cache=cache)

    def set_rigidity_run_params(self, highestMaxRigValue, maxRigValue, minRigValue, nIncrements_high, nIncrements_low):

        self._highestMaxRigValue = highestMaxRigValue
        self._maxRigValue = maxRigValue
        self._minRigValue = minRigValue
        self._nIncrements_high = nIncrements_high
        self._nIncrements_low = nIncrements_low

    def set_particle_direction_params(self, array_of_zeniths_and_azimuths):

        self._array_of_zeniths_and_azimuths = array_of_zeniths_and_azimuths

    def setMAGNETOCOSMICSdatetimeParameters(self,dateAndTime:dt.datetime,KpIndex:int):
        self._dateAndTime = dateAndTime
        self._KpIndex = KpIndex

    def setRunMode(self, runMode):
        self._runMode = runMode

    def set_MAGCOS_run_function(self, cache:bool):

        if cache == True:
            self.MAGCOS_run_callable = get_magcos_cache_function()
        else:
            self.MAGCOS_run_callable = MAGNETOCOSMICSrun

    def run(self, array_of_lats_and_longs:np.array):

        lowRigRun = self.MAGCOS_run_callable(array_of_lats_and_longs, self._array_of_zeniths_and_azimuths,
                                         self._date_and_time, self._kp_index,
                                         self._maxRigValue,self._minRigValue,self._nIncrements_low)

        highRigRun = self.MAGCOS_run_callable(array_of_lats_and_longs, self._array_of_zeniths_and_azimuths,
                                         self._date_and_time, self._kp_index,
                                         self._highestMaxRigValue,self._maxRigValue,self._nIncrements_high)

        highRigRun.full_rigidity_DF["Rlower"] = float(lowRigRun.full_rigidity_DF["Rlower"].iloc[0])
        highRigRun.full_rigidity_DF["Reffective"] = float(lowRigRun.full_rigidity_DF["Reffective"].iloc[0])
        highRigRun.full_rigidity_DF["Rupper"] = float(lowRigRun.full_rigidity_DF["Rupper"].iloc[0])
        
        self.fullRigidityDF = pd.concat([highRigRun.full_rigidity_DF,
                                         lowRigRun.full_rigidity_DF],ignore_index=True)

    def getOutputRigidities(self):
        return self.fullRigidityDF

if __name__ == "__main__":
    testMAGCOSrunManager = MAGNETOCOSMICSrunManager()
    testMAGCOSrunManager.run()

    print(testMAGCOSrunManager.getOutputRigidities())