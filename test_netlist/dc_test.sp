title

*netlist example 1
r2 2 1  2
v2 0 1  10
d1 0 2 modelname

.dc v2 -2 4 .2
.plot dc v(2) v(1)
.end