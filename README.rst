*************************************
SimulatedMotors Library (MiddleLayer)
*************************************

Description
===========
simulatedMotors library contains following simulated motors which can easily be used
in GUI, unit tests etc.

- SimulatedMotor
- SimulatedBeckhoffMC2Base
- SimulatedMultiAxisMotor
- SimulatedX2TimerML

Testing
=======

Every Karabo device in Python is shipped as a regular python package.
In order to make the device visible to any device-server you have to install
the package to Karabo's own Python environment.

Simply type:

``pip install -e .``

in the directory of where the ``setup.py`` file is located, or use the ``karabo``
utility script:

``karabo develop simulatedMotors``

Running
=======

If you want to manually start a server using these devices, simply type:

``karabo-middlelayerserver serverId=middleLayerServer/1 
deviceClasses=SimulatedMotor,SimulatedBeckhoffMC2Base,SimulatedMultiAxisMotor,SimulatedX2TimerML``

Or just use (a properly configured):

``karabo-start``
