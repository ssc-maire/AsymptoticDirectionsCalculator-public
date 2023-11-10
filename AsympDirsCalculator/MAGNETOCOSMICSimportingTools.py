

#from numba import jit

import numpy as np
import pandas as pd
import tqdm
import pickle as pkl
import multiprocessing as mp
import warnings


def pandasSeriesInputExtension(numpyOperationFunction):

    def pandasSeriesFunction(pandasSeries):

        return numpyOperationFunction(Xpla=pandasSeries["Xpla"],
                                      Ypla=pandasSeries["Ypla"],
                                      Zpla=pandasSeries["Zpla"])

    return pandasSeriesFunction

def disableAngleLimiting(angleLimitFunction):

    def skipFunction(value):

        return value

    return skipFunction

@disableAngleLimiting
def sinArcSin(value):
    
    valueInRad = 2*np.pi*value/360
    
    outputValue = np.arcsin(np.sin(valueInRad))
    
    outputValueInDeg = outputValue * 360 / (2*np.pi)
    
    return outputValueInDeg

@disableAngleLimiting
def cosArcCos(value):
    
    valueInRad = 2*np.pi*value/360
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        outputValue = np.arccos(np.cos(valueInRad))
    
    outputValueInDeg = outputValue * 360 / (2*np.pi)
    
    return outputValueInDeg

#@jit(nopython=True)
def getZenithStringFromFilePath(filePath):
    
    zenithString = filePath.split("_")[1]
    
    return zenithString

#@jit(nopython=True)
def getAzimuthStringFromFilePath(filePath):
    
    azimuthString = (filePath.split("_")[2]).split(".out")[0]
    
    return azimuthString

@pandasSeriesInputExtension
#@jit(nopython=True)
def calculateTHETAplaOfRow(Xpla, Ypla, Zpla):
    
    #return np.arctan(np.sqrt(row["Xpla"]**2+row["Ypla"]**2)/row["Zpla"]) * 360/ (2* np.pi)
    return np.arctan(np.sqrt(Xpla**2+Ypla**2)/Zpla) * 360/ (2* np.pi)
    
@pandasSeriesInputExtension
#@jit(nopython=True)
def calculatePHIplaOfRow(Xpla, Ypla, Zpla):
    
    if Xpla > 0:
        
        outputValue = np.arctan(Ypla/Xpla)
        
    elif Xpla < 0:
            
        outputValue = np.arctan(Ypla/Xpla)+np.pi
    
    else:
        
        outputValue = np.pi/2
        
    return outputValue * 360/(2*np.pi)

def calculateAngleBetweenPosAndMom(row):
    
    degreesToRad = 2 * np.pi / 360
    
    thetaOne = row["Lat"] * degreesToRad
    thetaTwo = row["THETApla"] * degreesToRad
    phiOne = row["Long"] * degreesToRad
    phiTwo = row["PHIpla"] * degreesToRad
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return finishPosMomAngleCalculation(thetaOne, thetaTwo, phiOne, phiTwo)

#@jit(nopython=True)
def finishPosMomAngleCalculation(thetaOne, thetaTwo, phiOne, phiTwo):
    return np.arccos((np.sin(thetaOne) * np.sin(thetaTwo) * np.cos(phiOne - phiTwo)) + 
            (np.cos(thetaOne) * np.cos(thetaTwo)))

def readOutputAngleFile(filePath):
    outputDF = pd.read_csv(filePath, 
            delimiter="\s+",
            index_col=False,
            skipfooter=1,
            header=None, 
            skiprows=1,
            engine="python")
            #engine="C")
    outputDF.columns = ["Rigidity","Filter","Lat", "Long", "Xpla", "Ypla", "Zpla"]
    
    #outputDF["Long"] = outputDF["Long"].apply(ifLessAdd)
    #outputDF["Long"] = outputDF["Long"].apply(sinArcSin)
    
    outputDF["Long"] = outputDF["Long"].apply(cosArcCos)
    outputDF["Lat"] = outputDF["Lat"].apply(sinArcSin)
    
    outputDF["initialZenith"] = getZenithStringFromFilePath(filePath)
    outputDF["initialAzimuth"] = getAzimuthStringFromFilePath(filePath)
    
    outputDF.zenith = getZenithStringFromFilePath(filePath)
    outputDF.azimuth = getAzimuthStringFromFilePath(filePath)
    
    outputDF["THETApla"] = outputDF.apply(lambda x:calculateTHETAplaOfRow(x),axis=1)
    #fullDF["PHIpla"] = np.piecewise(fullDF["Xpla"],
    #                                [fullDF["Xpla"] > 0, fullDF["Xpla"] < 0, fullDF["Xpla"] == 0.0],
    #                                [np.arctan(fullDF["Ypla"]/fullDF["Xpla"]),
    #                                 np.arctan(fullDF["Ypla"]/fullDF["Xpla"])+np.pi,
    #                                 np.pi/2])
    outputDF["PHIpla"] = outputDF.apply(lambda x:calculatePHIplaOfRow(x),axis=1)
    
    outputDF["angleDiffRad"] = outputDF.apply(lambda x:calculateAngleBetweenPosAndMom(x),axis=1)
    
    outputDF["weightingFactor"] = np.sin(2 * outputDF["angleDiffRad"])
    
    return outputDF[outputDF["Filter"] == 1]

def getPosAndMomDirFromFilename(filePath):

    latitude = float(filePath.split("POS_")[1].split("_")[0])
    longitude = float(filePath.split("POS_")[1].split("_")[1])
    zenith = float(filePath.split("MOM_")[1].split("_")[0])
    azimuth = float(filePath.split("MOM_")[1].split("_")[1].split(".")[0])

    return latitude, longitude, zenith, azimuth

def read_cutoff_values_from_file(filePath):

    with open(filePath, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]

    splitLastLine = last_line.split()

    rigidityDict = {"Rl":float(splitLastLine[1]),
                    "Rc":float(splitLastLine[3]),
                    "Ru":float(splitLastLine[5]),}

    return rigidityDict

def readNewOutputAngleFile(filePath):

    #print(filePath)
    
    outputDF = pd.read_csv(filePath, 
            delimiter="\s+",
            index_col=False,
            skipfooter=1,
            header=None, 
            skiprows=1,
            engine="python")
            #engine="C")
    
    outputDF.columns = ["Rigidity","Filter","Lat", "Long", "Xpla", "Ypla", "Zpla"]
    
    outputDF["Long"] = outputDF["Long"].apply(cosArcCos)
    outputDF["Lat"] = outputDF["Lat"].apply(sinArcSin)

    outputDF.latitude, outputDF.longitude, outputDF.zenith, outputDF.azimuth = getPosAndMomDirFromFilename(filePath)
    outputDF["initialLatitude"] = outputDF.latitude
    outputDF["initialLongitude"] = outputDF.longitude
    outputDF["initialZenith"] = outputDF.zenith
    outputDF["initialAzimuth"] = outputDF.azimuth
    
    outputDF["THETApla"] = outputDF.apply(lambda x:calculateTHETAplaOfRow(x),axis=1)
    outputDF["PHIpla"] = outputDF.apply(lambda x:calculatePHIplaOfRow(x),axis=1)
    
    outputDF["angleDiffRad"] = outputDF.apply(lambda x:calculateAngleBetweenPosAndMom(x),axis=1)
    
    outputDF["weightingFactor"] = np.sin(2 * outputDF["angleDiffRad"])

    rigidity_cutoff_dict = read_cutoff_values_from_file(filePath)

    outputDF["Rlower"] = rigidity_cutoff_dict["Rl"]
    outputDF["Reffective"] = rigidity_cutoff_dict["Rc"]
    outputDF["Rupper"] = rigidity_cutoff_dict["Ru"]
    
    return outputDF

#@mem.cache
def readLotsOfOutputAngleFiles(listOfFilePaths):
    listOfAllDFs = [readNewOutputAngleFile(filePath) for filePath in listOfFilePaths]
    #with mp.Pool(processes=4) as mpPool:
    #    listOfAllDFs = mpPool.map(pd.read_csv,listOfFilePaths)

    return pd.concat(listOfAllDFs)

#@mem.cache
def readLotsOfOutputAngleFilesChunked(listOfFilePaths,nChunks=100, save_as_pkl=False):

    chunkedListOfFilePaths = np.array_split(listOfFilePaths,
                                            min(nChunks,len(listOfFilePaths)))

    listOfAllDFs = [readLotsOfOutputAngleFiles(filePath) for filePath in tqdm.tqdm(chunkedListOfFilePaths) if len(filePath) != 0]
    with mp.Pool(processes=5) as mpPool:
        listOfAllDFs = mpPool.map(readLotsOfOutputAngleFiles,tqdm.tqdm(chunkedListOfFilePaths))

    fullDF = pd.concat(listOfAllDFs)

    if save_as_pkl == True:
        with open("savedFullDFlist.pkl", "wb") as f:
            pkl.dump(fullDF,f)

    return fullDF