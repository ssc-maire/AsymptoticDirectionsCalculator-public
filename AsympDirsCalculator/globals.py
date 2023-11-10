import os
import pkg_resources

global _magnetocosmicsShellScriptPath, \
       originalDirectory, \
       magcosRunDir

_magnetocosmicsShellScriptPath = pkg_resources.resource_filename(__name__,"magcos_running_scripts/runNoRewriteMAGCOSsimulation.sh")

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
