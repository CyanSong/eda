title

*netlist example 1

*m1 3 2 0 0 nm
*m2 3 2 4 4 pm
*vdd 4 0 1.8
*vgs 2 0 pulse(0 1.8 0 1m 1m 20m 40m)
*r1 3 0 10000000
*.tran .02 0.2 0 .01
*.plot tran   v(3) v(2)

r1 1 0 1
c1 2 1 1
v1 2 0 1
.tran .5 6
.plot tran v(1) v(2)

.end