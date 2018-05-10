title

*netlist example 1


m1 3 2 0 0 nm l=2.4 w=1
m2 3 2 4 4 pm l=1 w=1
vdd 4 0 1.8
vin 2 0 0.9
r1 3 0 5g
.dc vin 0 1.8 .05
.plot dc   v(3) v(2)
.end