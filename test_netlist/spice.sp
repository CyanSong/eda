title

*netlist example 1
r2 2 1  2
v2 0 1  10
c1 0 2 1

*.tran .01 2 0 0.002
*.plot tran v(1) v(2)

.dc v2 -2 4 .2
.plot dc i(v2)

*.ac 10000 0.1 20
*.plot ac v(1) v(2)


.end