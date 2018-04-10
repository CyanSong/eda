title

*netlist example 1
r1 0 1  1
r2 1 2  0.5
i2 1 2  1
d1 2 0 modelname

.dc i2 1 2 .2
.plot dc v(2) v(1)
.end