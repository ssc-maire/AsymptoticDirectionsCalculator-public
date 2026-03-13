import importlib.resources
import os

global _magnetocosmicsShellScriptPath, \
       originalDirectory, \
       magcosRunDir

_magnetocosmicsShellScriptPath = str(importlib.resources.files(__package__) / "magcos_running_scripts/runNoRewriteMAGCOSsimulation.sh")

originalDirectory = os.getcwd()

def getUniqueLabelForRunDir():

    runDirLabel = 1
    runDirToLookFor = f"{originalDirectory}/magnetocosmicsRunDir_{runDirLabel}"

    while os.path.exists(runDirToLookFor):
        runDirLabel += 1
        runDirToLookFor = f"{originalDirectory}/magnetocosmicsRunDir_{runDirLabel}"

    return runDirLabel
    
runDirLabel = getUniqueLabelForRunDir()
magcosRunDir = f"{originalDirectory}/magnetocosmicsRunDir_{runDirLabel}"
