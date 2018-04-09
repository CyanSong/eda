title

*netlist example 1
c2 2 0  2
i2 0 1  10
d1 1 2 modelname

.tran .01 2 0 0.002
.plot tran v(2) v(1)
.end