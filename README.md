# eda
**Overview**
This prjoct is for EDA course in SJTU.
The purpose of this project is to design a naive spice simulator.
The copyright is owned by the author Cyan Song.
### Installation
**First you should install matplotlib manually.**
To install the package:
```bash
python setup.py install
```
### Usage 
import the package:
```python
import xspice.xspice as xp
```
build the circuit and run commands:
```python
circuit = xp.Xspice("netlist_string")
circuit.handle_cmds()
```


