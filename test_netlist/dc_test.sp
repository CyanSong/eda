title

*netlist example 1


m1 3 2 0 0 nm
vdd 4 0 1.8
vgs 2 0 0.9
r1 3 4 50k
.dc vgs 0 1.8 .05
.plot dc   v(3)
.end