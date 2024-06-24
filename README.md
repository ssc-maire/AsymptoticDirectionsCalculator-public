# AsymptoticDirectionsCalculator

**N.B. Currently this tool only runs on Linux-based machines (if you are a Windows user, you must use [Windows Subsystem for Linux](https://ubuntu.com/wsl) or a virtual machine with Linux to install and run this tool)**

A Python toolkit for calculating both cut-off rigidities and asymptotic directions from any latitude and longitude on Earth's surface. This toolkit essentially acts as a Python wrapper for the Geant4-based magnetocosmics Monte Carlo software, which is popular within scientific fields that frequently need to perform calculations of particle trajectories in Earth's magnetic field. Magnetocosmics here calculates asymptotic directions using the commonly used method of backtracing the trajectory of a particle with a particular magnetic rigidity from a particular location on Earth's surface.

This toolkit currently only runs the Tsyganenko 1989 model, and the IGRF model to supply magnetocosmics with the current status of Earth's magnetic field, although the model could be quite easily extended to use other models already contained within magnetocosmics in the future. TSY89 and IGRF only require a particular date and time, as well as the current value of Kp index (a single number that describes the current conditions of Earth's magnetic field) to describe Earth's magnetic field at a given time. Note that this toolkit may need to be updated in 2025 with the latest values for the IGRF model of Earth's geomagnetic (internal field), otherwise calculations may fail. 

**To use this package you must have a version of magnetocosmics installed, such that magnetocosmics can be run by typing 'magnetocosmics' the terminal, i.e. typing:**

```
$ magnetocosmics
```
outputs something like the following:
```


          ################################
          !!! G4Backtrace is activated !!!
          ################################


**************************************************************
 Geant4 version Name: geant4-11-00-patch-02 [MT]   (25-May-2022)
                       Copyright : Geant4 Collaboration
                      References : NIM A 506 (2003), 250-303
                                 : IEEE-TNS 53 (2006), 270-278
                                 : NIM A 835 (2016), 186-225
                             WWW : http://geant4.org/
**************************************************************

/h n m 1900.0 1905.0 1910.0 1915.0 1920.0 1925.0 1930.0 1935.0 1940.0 1945.0 1950.0 1955.0 1960.0 1965.0 1970.0 1975.0 1980.0 1985.0 1990.0 1995.0   2000.0    2005.0    2010.0    2015.0   2020.0    SV
mmm1900
Nyear 25
1900
Nyear 25

...

g       8       8
h       8       8
g       9       0
0.0     0       -999
XGSE in GEI (0.193332,-0.900173,-0.39027)
(0.0573796,-0.172205,0.983389)
-19.4809
Selected index20
XGSE in GEI (0.17509,-0.903305,-0.391643)
(0.0590434,-0.175608,0.982688)
-25.9091
Test93
Test97
Test
G4CashKarpRKF45 is called
```

While this package is new, it fundamentally relies on Magnetocosmics, which is no longer maintained, and it is therefore likely that the community will eventually create a successor for Magnetocosmics. One attempt to do this is the [OTSO software](https://github.com/NLarsen15/OTSO), which is also designed to be open-source and community oriented. We hope that in the future, OTSO may succeed this software, or even that this Python wrapper could be integrated with OTSO. 

## Installation

To install this toolkit through the normal [PyPi method](https://pypi.org/project/AsympDirsCalculator/), you can simply run

```
sudo pip install AsympDirsCalculator
```

Alternatively, to install this toolkit directly from this Github repository you can first clone the repository, and then from the cloned respository, run

```
sudo pip3 install .
```

in the cloned directory. 

Note that there are quite a few sizeable data files within this package that get copied during installation (on the order of about several hundred megabytes in total) so installation may take a couple of minutes.

## Usage

After installation, to import the toolkit in a particular Python script, run 
```
from AsympDirsCalculator import AsympDirsTools
```
Both of the main useful functions to users are contained within the `AsympDirsTools` module, and all other modules contained in this toolkit are primarily intended to be accessed internally (although don't let that stop you from using or editing them for your own purposes if you wish).

### Calculating asymptotic directions

The main function for calculating asymptotic directions is the `get_magcos_asymp_dirs` function. 

A full example of its usage is given below (a simpler example is shown afterwards). Note that the rigidities to calculate for are here defined by a low set of rigidities and a high set of rigidities. The high set of rigidities are generated linearly between the value of `maxRigValue` and `highestMaxRigValue`. The low set of rigidities are generated linearly between `minRigValue` and `maxRigValue`. The numbers of rigidities generated in the high set of rigidities and low set of rigidities are defined by `nIncrements_high` and `nIncrements_low` respectively.
```
import numpy as np
import datetime as dt

AsympDirsTools.get_magcos_asymp_dirs(
    array_of_lats_and_longs=np.array(np.meshgrid(np.linspace(-90.0, 90.0, 37), np.linspace(0.0, 355.0, 72))).T.reshape(-1, 2),
    array_of_zeniths_and_azimuths=np.array([[0.0, 0.0]]),
    KpIndex=2,
    dateAndTime=dt.datetime.now(),
    highestMaxRigValue=1010,
    maxRigValue=20,
    minRigValue=0.1,
    nIncrements_high=60,
    nIncrements_low=200,
    cache=False,
    full_output=False,
)
```
* `array_of_lats_and_longs` : `numpy.ndarray` (default=`np.array(np.meshgrid(np.linspace(-90.0, 90.0, 37), np.linspace(0.0, 355.0, 72))).T.reshape(-1, 2)`)  
A 2D array of latitude and longitude values (can also be specified as a Python list) defining the latitudes and longitudes that asymptotic directories should be calculated at. By default this is set to calculate for a grid of values covering a grid of Earth's surface.

* `array_of_zeniths_and_azimuths` : `numpy.ndarray` (default=`np.array([[0.0, 0.0]])`)  
A 2D array of zenith and azimuth values, for defining the initial particle momentum directions away from Earth's surface to perform calculations for. By default this is set to 0.0 to represent vertical asymptotic directions.

* `KpIndex` : `int` (default=`2`)  
The value of Kp index to use.

* `dateAndTime` : `datetime.datetime` (default=`datetime.datetime.now()`)  
The date and time for the magnetic field to use for the run.

* `highestMaxRigValue` : `int` (default=`1010`)  
The highest maximum rigidity value.

* `maxRigValue` : `int` (default=`20`)  
The maximum rigidity value.

* `minRigValue` : `float` (default=`0.1`)  
The minimum rigidity value.

* `nIncrements_high` : `int` (default=`60`)  
The number of increments for the high rigidity values.

* `nIncrements_low` : `int` (default=`200`)  
The number of increments for the low rigidity values.

* `cache` : `bool` (default=`False`)  
Boolean value to indicate whether to cache the run.

* `full_output` : `bool` (default=`False`)  
Boolean value to print an extended set of output data containing more output parameters.

A simple example of its usage might be the following:
```
from AsympDirsCalculator import AsympDirsTools

lats_and_longs_to_calc_asymp_dirs_at = [[0.0, 0.0],[1.0,1.0],[50.0,0.0]]
asymp_dirs_DF = AsympDirsTools.get_magcos_asymp_dirs(array_of_lats_and_longs = lats_and_longs_to_calc_asymp_dirs_at)

print(asymp_dirs_DF)
```
Here `AsympDirsTools.get_magcos_asymp_dirs` returns a Pandas Dataframe containing the vertical asymptotic directions (`array_of_zeniths_and_azimuths` is set to give vertical asymptotic directions by default) for a range of possible particle rigidities in terms of latitude and longitude for each of the supplied input coordinates. The example here prints this dataframe to standard output:

```
     initialLatitude  initialLongitude  ...        Long  Filter
59               0.0               0.0  ...    1.404392       1
60               0.0               0.0  ...    1.428121       1
61               0.0               0.0  ...    1.452666       1
62               0.0               0.0  ...    1.478070       1
63               0.0               0.0  ...    1.504378       1
..               ...               ...  ...         ...     ...
371             50.0               0.0  ...  170.320243       0
372             50.0               0.0  ...  175.506896       0
373             50.0               0.0  ... -156.058870       0
374             50.0               0.0  ...  165.680388       0
375             50.0               0.0  ...  167.508689       0

[774 rows x 6 columns]
```

Here the full dataframe does not get shown by a print statement, as the dataframe is quite large. 

The full output columns are:

* `initialLatitude`, `initialLongitude`: The location on Earth's surface the asymptotic direction is referring to/the initial location on Earth's surface the particle was generated at. These are identical to the latitudes and longitudes that were input into the function in the first place.
* `Rigidity`: The particle rigidity in units of gigavolts (GV) that were used to calculate the asymptotic direction in this instance
* `Lat`: The asymptotic latitude of the particle
* `Long`: The asymptotic longitude of the particle
* `Filter`: A 1 or a 0, indicating whether or not the particle successfully exited Earth's magnetosphere (a 1 means the particle exited ).

Unless otherwise stated, all angles given in results are in degrees, and all rigidities are specified in gigavolts (GV).

For an extended output, you can add the set the optional input argument `full_output=True` to the function. In the case of the example code above, this will return

```
        Rigidity  Filter        Lat  ...  Rlower  Reffective  Rupper
59   1010.000000       1   0.156057  ...     3.1         3.2     3.3
60    993.220339       1   0.158726  ...     3.1         3.2     3.3
61    976.440678       1   0.161488  ...     3.1         3.2     3.3
62    959.661017       1   0.164348  ...     3.1         3.2     3.3
63    942.881356       1   0.167311  ...     3.1         3.2     3.3
..           ...     ...        ...  ...     ...         ...     ...
371     0.600000       0  24.022842  ...     3.1         3.2     3.3
372     0.500000       0   1.069429  ...     3.1         3.2     3.3
373     0.400000       0  15.502665  ...     3.1         3.2     3.3
374     0.300000       0  15.259742  ...     3.1         3.2     3.3
375     0.200000       0   7.577144  ...     3.1         3.2     3.3

[774 rows x 18 columns]
```
The full list of columns that get outputted here are:

* `Rigidity`: The particle rigidity in units of gigavolts (GV) that were used to calculate the asymptotic direction in this instance.
* `Filter`: A 1 or a 0, indicating whether or not the particle successfully exited Earth's magnetosphere.
* `Lat`: The asymptotic latitude of the particle.
* `Long`: The asymptotic longitude of the particle.
* `Xpla`, `Ypla`, `Zpla`: The final position the particle reached in GEO coordinates.
* `initialLatitude`, `initialLongitude`: The location on Earth's surface the asymptotic direction is referring to/the initial location on Earth's surface the particle was generated at. These are identical to the latitudes and longitudes that were input into the function in the first place.
* `initialZenith`, `initialAzimuth`: The directions the particles were originally generated to be travelling at, in spherical coordinates away from Earth's surface. These are currently always set to be equal to 0.0, to represent a particle travelling vertically, i.e. calculating specifically the vertical asymptotic direction. In the future however the scope of this program could be increased to include non-vertical asymptotic directions.
* `THETApla`, `PHIpla`: The final position the particle reached, but in spherical coordinates (i.e. latitude and longitude).
* `angleDiffRad`: The angle between the location where the particle exited the simulation geometry (in Earth-centered spherical coordinates), and its momentum direction.
* `weightingFactor`: A column containing a weighting factor relating to how connected the computed trajectory would be to incoming trajectories in an isotropic distribution. This column is likely not needed for users except in extremely advanced contexts.
* `Rlower`: The lowest rigidity of particle that successfully exited Earth's magnetosphere
* `Reffective`: The mean rigidity of particle that successfully exited Earth's magnetosphere, between Rlower and Rupper
* `Rupper`: The lowest rigidity of particle that failed to successfully exit Earth's magnetosphere

### Calculating cut-off rigidities

While the extended output for the previous function does produce cut-off rigidities, a simpler way to calculate cut-off rigidities is to use the `get_magcos_vcutoffs` function.

It should be noted that currently cut-off rigidities are only calculated to a minimum resolution of 0.1 GV, and also that any cut-off rigidities lower than 0.2 GV are set to equal 0 by the current code. This should be updated in future versions of this software.

`get_magcos_vcutoffs` takes exactly the same input parameters as `get_magcos_asymp_dirs`, but outputs the cut-off rigidities at a particular location, rather than asymptotic directions. For example, the code

```
from AsympDirsCalculator import AsympDirsTools

lats_and_longs_to_calc_asymp_dirs_at = [[0.0, 0.0],[1.0,1.0],[50.0,0.0]]
vcutoffs_DF = AsympDirsTools.get_magcos_vcutoffs(array_of_lats_and_longs = lats_and_longs_to_calc_asymp_dirs_at)

print(vcutoffs_DF)
```

will print

```
                                  Rlower  Reffective  Rupper
initialLatitude initialLongitude                            
0.0             0.0                 13.2        13.2    13.2
1.0             1.0                 13.4        13.4    13.4
50.0            0.0                  3.1         3.2     3.3
```

to standard output.

Here, the outputted vertical cut-off rigidity columns refer to
* `Rlower`: The lowest rigidity of particle that successfully exited Earth's magnetosphere
* `Reffective`: The mean rigidity of particle that successfully exited Earth's magnetosphere, between `Rlower` and `Rupper`
* `Rupper`: The lowest rigidity of particle that failed to successfully exit Earth's magnetosphere

## References

Desorgher, L. MAGNETOCOSMICS Users Manual. (University of Bern, 2006)
