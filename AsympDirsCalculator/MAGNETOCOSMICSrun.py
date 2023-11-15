
from distutils import dir_util
import os
from pathlib import Path
import glob as gb
import shutil
import subprocess

from joblib import Memory

from .MAGCOSmacroFileGenerator import MAGCOSmacroFileGenerator
from .MAGNETOCOSMICSimportingTools import readLotsOfOutputAngleFilesChunked

from .globals import _magnetocosmicsShellScriptPath, magcosRunDir, originalDirectory

def get_magcos_cache_function():
    MAGCOScachedir = f"{os.getcwd()}/cachedMagnetocosmicsRunData"
    MAGCOSmemory = Memory(MAGCOScachedir, verbose=0)

    @MAGCOSmemory.cache()
    def run_or_get_MAGNETOCOSMICS_cache(*args, **kwargs):

        the_MAGCOS_run = MAGNETOCOSMICSrun(*args, **kwargs)

        return the_MAGCOS_run

    return run_or_get_MAGNETOCOSMICS_cache

class MAGNETOCOSMICSrun():

    def __init__(self, 
                array_of_lats_and_longs, array_of_zeniths_and_azimuths, 
                date_and_time,KpIndex,
                maxRigValue,minRigValue,nIncrements):

        Path(f"{magcosRunDir}/magcos_running_scripts/outputFiles/").mkdir(parents=True, exist_ok=True)
        Path(f"{magcosRunDir}/data/").mkdir(parents=True, exist_ok=True)
        Path(f"{magcosRunDir}/bin/").mkdir(parents=True, exist_ok=True)

        os.chdir(f"{magcosRunDir}/magcos_running_scripts/")

        for previousOutputFile in gb.glob(magcosRunDir + "/magcos_running_scripts/outputFiles/*.out"):
            os.remove(previousOutputFile)

        macroFileGenerator = MAGCOSmacroFileGenerator()
        macroFileGenerator.setMAGNETOCOSMICSdatetimeParameters(date_and_time,KpIndex=KpIndex)
        macroFileGenerator.setRigidityVectorString(maxRigValue, minRigValue, nIncrements)

        macroFileGenerator.generateMacro(array_of_lats_and_longs, array_of_zeniths_and_azimuths)

        try:
            magnetocosmics_subprocess_run = subprocess.run(_magnetocosmicsShellScriptPath)
            assert magnetocosmics_subprocess_run.returncode == 0
        except:
            raise Exception("ERROR: running magnetocosmics and processing output files failed, please check the above error messages to debug what might have gone wrong.")

        os.chdir(originalDirectory)

        self.full_rigidity_DF = self.importMAGCOSoutputFiles()

        shutil.rmtree(magcosRunDir)

    def importMAGCOSoutputFiles(self):
        listOfAllFilesToImport = gb.glob(f"{magcosRunDir}/magcos_running_scripts/outputFiles/*.out")
        print("Importing all Magnetocosmics output files to a dataframe...")
        fullRigidityDFGEO = readLotsOfOutputAngleFilesChunked(listOfAllFilesToImport,nChunks=100)
        print("Magnetocosmics importing completed.")

        return fullRigidityDFGEO

    def get_full_rigidity_DF(self):
        return self.full_rigidity_DF