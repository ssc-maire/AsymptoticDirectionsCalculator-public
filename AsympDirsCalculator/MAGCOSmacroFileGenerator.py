import datetime as dt

import numpy as np
import pkg_resources

from .globals import magcosRunDir

class MAGCOSmacroFileGenerator():

    _MacroFileTemplateLocation = pkg_resources.resource_filename(__name__,"magcos_running_scripts/AsymptoticDirection.g4mac")

    def __init__(self):
        with open(self._MacroFileTemplateLocation,"r") as templateFile:
            macroFileTemplateString = templateFile.read()
        macroFileSplit = macroFileTemplateString.split("REPLACE_THIS_LINE_WITH_FULL_LOOP_COMMANDS")
        self._MacroFilePrefix = macroFileSplit[0]
        self._MacroFileSuffix = macroFileSplit[1]

    def setZenithList(self,zenithList):
        self._zenithList = zenithList

    def setAzimuthList(self,azimuthList):
        self._azimuthList = azimuthList

    def setLatitudeList(self,latitudeList):
        self._latitudeList = latitudeList

    def setLongitudeList(self,longitudeList):
        self._longitudeList = longitudeList

    def setIopt(self, Iopt):
        self._Iopt = Iopt

    def setDatetime(self, dateAndTime:dt.datetime):
        self._dateAndTime = dateAndTime

    def setRigidityVectorString(self,maxValue:float,minValue:float,nIncrements:int):

        increment = (minValue - maxValue)/(nIncrements - 1)

        self._rigidityVectorString = "\n/MAGCOS/RIGIDITYVECTOR/Reset\n/MAGCOS/RIGIDITYVECTOR/AddValues " + \
                                     str(maxValue) + " " + \
                                     str(increment) + " " + \
                                     str(nIncrements-1) + "\n"

    def setMAGNETOCOSMICSdatetimeParameters(self,dateAndTime:dt.datetime,KpIndex:int):
        self.setDatetime(dateAndTime)
        self.setIopt(KpIndex+1)

    def setMishevMAGNETOCOSMICSParameters(self):
        self.setDefaultMAGNETOCOSMICSrunParameters()
        self.setMAGNETOCOSMICSdatetimeParameters(self._dateAndTime,
                                                KpIndex=4)
    
    # def setDefaultMAGNETOCOSMICSrunParameters(self,maxValue,minValue,nIncrements):
    #     self.setZenithList([0.0])
    #     self.setAzimuthList([0.0])
    #     self.setLatitudeList(np.linspace(-90.0,90.0,37))
    #     self.setLongitudeList(np.linspace(0.0,355.0,72))
    #     self.setRigidityVectorString(maxValue=maxValue,minValue=minValue,nIncrements=nIncrements)

    def setTestMAGNETOCOSMICSrunParameters(self):
        self.setDefaultMAGNETOCOSMICSrunParameters()
        self.setMAGNETOCOSMICSdatetimeParameters(self._dateAndTime,
                                                KpIndex=6)

    def getSingleRunString(self,zenith,azimuth,latitude,longitude):

        runSetupString = "\n/MAGCOS/SOURCE/SetPosition GEOID 100. km " + \
                                    str(latitude) + " " + \
                                    str(longitude) + \
                                    " degree\n/MAGCOS/SOURCE/SetDirection GEOID " + \
                                    str(zenith) + " " + \
                                    str(azimuth) + \
                                    " degree\n"
                                    
        runString = "/MAGCOS/SCENARIO/ComputeAsymptoticDirections AsymptoticDirectionDay_POS_" + \
                        str(latitude) + "_" + \
                        str(longitude) + \
                        "_MOM_" + \
                        str(zenith) + "_" + \
                        str(azimuth) + ".out"

        return runSetupString + runString

    def getMagnetosphericConditionsString(self):

        IoptString = f"/MAGCOS/BFIELD/SetIopt {self._Iopt}"
        datetimeString = f"/MAGCOS/BFIELD/SetStartDate {self._dateAndTime.year} {self._dateAndTime.month} {self._dateAndTime.day} {self._dateAndTime.hour} {self._dateAndTime.minute} {self._dateAndTime.second}"
        magFieldSpecificationString = "\n" + IoptString + "\n" + datetimeString + "\n"
        return magFieldSpecificationString

    def generateMacro(self, lat_and_long_list, zenith_and_azimuth_list):

        magFieldSpecificationString = self.getMagnetosphericConditionsString()

        fullRunningString = ""

        for zenith, azimuth in zenith_and_azimuth_list:
            for latitude, longitude in lat_and_long_list:
                fullRunningString += self.getSingleRunString(zenith, azimuth, latitude, longitude)
        
        fullMacroString = self._MacroFilePrefix + magFieldSpecificationString + self._rigidityVectorString + fullRunningString + self._MacroFileSuffix

        with open(magcosRunDir + "/magcos_running_scripts/runningAsymptoticDirection.g4mac","w") as outputMacroFile:
            outputMacroFile.write(fullMacroString)