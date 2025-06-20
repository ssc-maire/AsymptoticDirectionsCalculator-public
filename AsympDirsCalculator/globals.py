import os
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Python < 3.9
    import importlib_resources as pkg_resources

global _magnetocosmicsShellScriptPath, \
       originalDirectory, \
       magcosRunDir

try:
    # For Python 3.9+
    _magnetocosmicsShellScriptPath = str(pkg_resources.files(__name__) / "magcos_running_scripts/runNoRewriteMAGCOSsimulation.sh")
except AttributeError:
    # Fallback for older versions
    import pkg_resources as old_pkg_resources
    _magnetocosmicsShellScriptPath = old_pkg_resources.resource_filename(__name__,"magcos_running_scripts/runNoRewriteMAGCOSsimulation.sh")

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
