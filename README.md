# eda
**Overview**
<br>This prjoct is for EDA course in SJTU<br>
<br>The purpose of this project is to design a naive spice simulator with GUI.<br>
<br>The copyright is owned by the author Cyan Song.<br>
###Installation
<br>First you should install matplotlib manually.<br>
<br>Then```python setup.py install```to install the package<br>
###Usage 

<br>import the package:```python
import xspice.xspice as xp```<br>
<br>build the circuit and run commands```python
circuit = xp.Xspice("netlist_string")
circuit.handle_cmds()
```<br>


